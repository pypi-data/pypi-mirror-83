
from django.apps import apps

from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from customers.models import CustomerField

from exchange.utils import get_price_factory
from exchange.constants import CURRENCY_UAH
from exchange.models import MultiCurrencyPrice, ExchangeRates


app_config = apps.get_app_config('invoices')


class InvoiceField(models.ForeignKey):

    def __init__(
            self,
            to,
            verbose_name=_('Invoice'),
            on_delete=models.CASCADE,
            related_name='items',
            *args, **kwargs):

        super().__init__(
            to=to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            related_name=related_name,
            *args, **kwargs)


class InvoiceTypeField(models.PositiveIntegerField):

    def __init__(
            self,
            choices,
            verbose_name=_('Type'),
            *args, **kwargs):

        super().__init__(
            choices=choices,
            verbose_name=verbose_name,
            *args, **kwargs
        )


class Invoice(models.Model):

    type = NotImplemented
    customer = NotImplemented

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    discount = models.PositiveIntegerField(
        verbose_name=_('Discount, %'),
        default=0)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._old_type = self.type

    def save(self, **kwargs):
        if self.type != self._old_type:
            self.created = timezone.now()
        super().save(**kwargs)

    def __str__(self):
        return str(self.created)

    @classmethod
    def create(cls, type):
        return cls.objects.create(type=type)

    @property
    def invoice_type(self):
        return self.__class__.__name__.lower()

    @property
    def manage_url(self):
        return self._get_url('manage')

    @property
    def print_url(self):
        return self._get_url('print')

    @property
    def set_customer_url(self):
        return self._get_url('set-customer')

    @property
    def add_item_url(self):
        return self._get_url('add-item')

    @property
    def set_discount_url(self):
        return self._get_url('set-discount')

    def _get_url(self, name):
        return reverse_lazy('invoices:' + name, args=[
            self.invoice_type,
            self.pk
        ])

    @property
    def model_name(self):
        return self._meta.verbose_name

    @transaction.atomic
    def add_item(self, product, qty=1):
        try:
            item = self.items.get(product=product)
            item.qty += qty
            item.save()

        except ObjectDoesNotExist:
            item = self.items.create(
                product=product,
                qty=qty,
                **product.price_values
            )

        self._handle_add_item(product, qty)

        return item

    def _handle_add_item(self, product, qty):
        pass

    @transaction.atomic
    def set_item_qty(self, item_id, value):

        item = self.items.select_related('product').get(pk=item_id)

        if item.qty != value:
            self._handle_set_item_qty(item, value)

            item.qty = value
            item.save(update_fields=['qty'])

        return item

    @transaction.atomic
    def set_item_price(self, item_id, value):

        item = self.items.select_related('product').get(pk=item_id)

        if item.price_uah != value:
            self._handle_set_item_price(item, value)

            item.initial_currency = CURRENCY_UAH
            item.price_retail = value
            item.save(update_fields=['price_retail'])

            ExchangeRates.update_prices(self.items.filter(pk=item.pk))

        return item

    def _handle_set_item_qty(self, item, value):
        pass

    def _handle_set_item_price(self, item, value):
        pass

    @transaction.atomic
    def remove_item(self, item_id):

        item = self.items.select_related('product').get(pk=item_id)

        self._handle_remove_item(item)

        product = item.product

        item.delete()

        return product

    def _handle_remove_item(self, item):
        pass

    def set_customer(self, customer):

        self.customer = customer
        self.discount = self.customer_discount
        self.save(update_fields=['customer', 'discount'])

    @property
    def total(self):
        return sum([i.subtotal for i in self.items.all()])

    @property
    def discounted_total(self):
        return self.calculate_discount(self.total)

    @property
    def total_with_discount(self):
        return self.total - self.discounted_total

    @property
    def total_qty(self):
        return sum([i.qty for i in self.items.all()])

    @property
    def customer_discount(self):

        if self.customer:
            return self.customer.discount

        return 0

    def calculate_discount(self, number):

        if not self.discount:
            return 0

        return (self.discount * number) / 100.0

    def set_discount(self, value):
        self.discount = value
        self.save(update_fields=['discount'])

    def serialize_totals(self):
        return {
            'grand_total': self.total,
            'discount_percentage': self.discount,
            'discounted_total': self.discounted_total,
            'total_with_discount': self.total_with_discount
        }

    def get_items(self):
        return self.items.all().order_by('-id')

    class Meta:
        abstract = True


class InvoiceItem(MultiCurrencyPrice):

    invoice = NotImplemented

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('Product'),
        on_delete=models.CASCADE)

    qty = models.IntegerField(_('Quantity'))

    def set_rates(self, rates):
        self.rates = rates

    @property
    def product_name(self):
        return self.product.name

    @property
    def bar_code(self):
        return self.product.bar_code

    @property
    def set_qty_url(self):
        return reverse_lazy('invoices:set-item-qty', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    @property
    def set_price_url(self):
        return reverse_lazy('invoices:set-item-price', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    @property
    def remove_url(self):
        return reverse_lazy('invoices:remove-item', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    def calculate_discount(self, number):
        return self.invoice.calculate_discount(number)

    @property
    def price(self):
        price = super().price

        if self.currency == CURRENCY_UAH:
            return round(price)

        return price

    @property
    def price_with_discount(self):
        return self.price - self.calculate_discount(self.price)

    @property
    def subtotal(self):
        return self.price * self.qty

    @property
    def discounted_subtotal(self):
        return self.calculate_discount(self.subtotal)

    @property
    def subtotal_with_discount(self):
        return self.price_with_discount * self.qty

    @property
    def price_wholesale_uah(self):
        return get_price_factory(
            self.rates,
            self.initial_currency,
            CURRENCY_UAH
        )(self.price_wholesale)

    @property
    def wholesale_subtotal_uah(self):
         return self.price_wholesale_uah * self.qty

    @property
    def profit_uah(self):
        return self.price_with_discount - self.price_wholesale_uah

    @property
    def profit_subtotal_uah(self):
        return self.subtotal_with_discount - self.wholesale_subtotal_uah

    def render(self):
        return render_to_string('invoices/item.html', {'object': self})

    def serialize_product(self):
        return self.product.serialize()

    class Meta:
        abstract = True


class Arrival(Invoice):

    TYPE_INCOME = 1
    TYPE_RETURN = 2
    TYPE_CUSTOM = 3

    TYPES = (
        (TYPE_INCOME, _('Income')),
        (TYPE_RETURN, _('Return')),
        (TYPE_CUSTOM, _('Custom')),
    )

    type = InvoiceTypeField(TYPES)

    customer = CustomerField(related_name='arrivals')

    def _handle_add_item(self, product, qty):

        product.add_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if item.qty > value:
            item.product.subtract_stock(item.qty - value)
        else:
            item.product.add_stock(value - item.qty)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.subtract_stock(item.qty)

    class Meta:
        verbose_name = _('Arrival')
        verbose_name_plural = _('Arrivals')


class ArrivalItem(InvoiceItem):

    invoice = InvoiceField(Arrival)


class Sale(Invoice):

    TYPE_CASH_REGISTER = 1
    TYPE_WRITE_OFF = 2
    TYPE_ONLINE = 3
    TYPE_CUSTOM = 4
    TYPE_DEBT = 5

    TYPES = (
        (TYPE_CASH_REGISTER, _('Cash register')),
        (TYPE_WRITE_OFF, _('Write off')),
        (TYPE_DEBT, _('Debt')),
        (TYPE_CUSTOM, _('Custom')),
    )

    if app_config.is_online_sale_enabled:
        TYPES += ((TYPE_ONLINE, _('Online')), )

    type = InvoiceTypeField(TYPES)

    customer = CustomerField(related_name='sales')

    def _handle_add_item(self, product, qty):

        product.subtract_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if value > item.qty:
            item.product.subtract_stock(value - item.qty)
        else:
            item.product.add_stock(item.qty - value)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.add_stock(item.qty)

    @property
    def service_total(self):
        return sum([s.subtotal for s in self.services.all()])

    def set_customer(self, customer):
        super().set_customer(customer)
        self.services.all().update(customer=customer)

    def serialize_totals(self):
        totals = super().serialize_totals()
        totals['service_total'] = self.service_total
        return totals

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


class SaleItem(InvoiceItem):

    invoice = InvoiceField(Sale)
