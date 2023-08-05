
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from exchange.models import ExchangeRates
from pagination import paginate
from customers.forms import CustomerSelectForm

from invoices.forms import (
    SearchProductForm,
    ReportForm,
    InvoiceTypeSelectForm)
from invoices.models import (
    Sale,
    SaleItem,
    Arrival,
    ArrivalItem)

from apps.products.models import Product
from apps.site.views import render


@staff_member_required
def create_invoice(request, invoice_type):

    model = _get_invoice_model(invoice_type)

    form = InvoiceTypeSelectForm(model.TYPES, request.POST)

    if not form.is_valid():
        messages.error(request, 'Error')
        return redirect('home')

    invoice = model.objects.create(type=form.cleaned_data['type'])

    return redirect(invoice.manage_url)


@staff_member_required
def manage_invoice(request, invoice_type, invoice_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    customer_select_form = CustomerSelectForm(
        initial={'customer': invoice.customer})

    return render(request, 'invoices/manage/{}.html'.format(invoice_type), {
        'invoice': invoice,
        'invoice_type': invoice_type,
        'customer_select_form': customer_select_form
    })


@csrf_exempt
@require_POST
@staff_member_required
def set_customer(request, invoice_type, invoice_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    form = CustomerSelectForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest('Incorrect form')

    invoice.set_customer(form.cleaned_data['customer'])

    return JsonResponse({
        'message': _('Customer saved'),
        'total': invoice.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def set_discount(request, invoice_type, invoice_id):

    try:
        value = int(request.POST['value'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest(_('Incorrect value'))

    invoice = _get_invoice(invoice_type, invoice_id)

    invoice.set_discount(value)

    return JsonResponse({
        'message': _('Discount saved'),
        'total': invoice.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def add_item(request, invoice_type, invoice_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    try:
        item = invoice.add_item(product)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'status': 'OK',
        'html': item.render(),
        'item_id': item.id,
        'product': item.serialize_product(),
        'total': invoice.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def set_item_qty(request, invoice_type, invoice_id, item_id):

    try:
        value = int(request.POST['value'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest(_('Incorrect value'))

    invoice = _get_invoice(invoice_type, invoice_id)

    try:
        item = invoice.set_item_qty(item_id, value)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'message': _('Quantity updated'),
        'product': item.serialize_product(),
        'total': invoice.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def set_item_price(request, invoice_type, invoice_id, item_id):

    try:
        value = float(request.POST['value'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest(_('Incorrect value'))

    invoice = _get_invoice(invoice_type, invoice_id)

    try:
        item = invoice.set_item_price(item_id, value)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'message': _('Price updated'),
        'product': item.serialize_product(),
        'total': invoice.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def remove_item(request, invoice_type, invoice_id, item_id):

    invoice = _get_invoice(invoice_type, invoice_id)

    try:
        product = invoice.remove_item(item_id)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    return JsonResponse({
        'message': _('Item removed'),
        'product': product.serialize(),
        'total': invoice.serialize_totals()
    })


@staff_member_required
def get_products(request):

    form = SearchProductForm(data=request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest('Invalid form')

    queryset = Product.objects.active().search(**form.cleaned_data)

    page = paginate(request, queryset, per_page=50)

    return JsonResponse({
        'items': render_to_string('invoices/product-items.html', {
            'page_obj': page
        }),
        'has_next': page.has_next(),
        'next_page_url': '{}?{}'.format(
            request.path, page.next_page_number().querystring)
    })


@staff_member_required
def print_invoice(request, invoice_type, invoice_id):
    return render(request, 'invoices/print.html', {
        'invoice': _get_invoice(invoice_type, invoice_id),
        'invoice_type': invoice_type
    })


@staff_member_required
def get_report(request, invoice_type):

    form = ReportForm(request)

    invoice_model = _get_invoice_model(invoice_type)

    exclude_types = [
        invoice_model.TYPE_CUSTOM
    ]

    if invoice_type == 'sale':
        exclude_types += [
            invoice_model.TYPE_DEBT,
            invoice_model.TYPE_WRITE_OFF
        ]

    items = _get_invoice_items(
        _get_invoice_item_model(invoice_type),
        form,
        exclude_types=exclude_types)

    totals = _get_invoice_totals(items)

    context = {
        'form': form,
        'items': items,
        'totals': totals
    }

    context.update(form.cleaned_data)

    if invoice_type == 'sale':

        return_items = _get_invoice_items(
            ArrivalItem, form, invoice_type=Arrival.TYPE_RETURN)

        return_totals = _get_invoice_totals(return_items)

        write_off_items = _get_invoice_items(
            SaleItem, form, invoice_type=Sale.TYPE_WRITE_OFF)

        write_off_totals = _get_invoice_totals(write_off_items)

        context.update({
            'return_items': return_items,
            'return_totals': return_totals,
            'write_off_items': write_off_items,
            'write_off_totals': write_off_totals,
            'grand_totals': {
                'qty': totals['qty'] - return_totals['qty'],
                'wholesale_total': (
                    totals['wholesale_total'] -
                    return_totals['wholesale_total']),
                'retail_total': (
                    totals['retail_total'] - return_totals['retail_total']),
                'profit_total': (
                    totals['profit_total'] - return_totals['profit_total'])
            }
        })

    return render(
        request, 'invoices/report/{}-report.html'.format(invoice_type), context)


def _get_invoice_items(model, form, invoice_type=None, exclude_types=None):

    items = model.objects.filter(
        invoice__created__date__range=[
            form.cleaned_data['date_from'],
            form.cleaned_data['date_to']
        ]
    )

    if invoice_type is not None:
        items = items.filter(invoice__type=invoice_type)

    if exclude_types is not None:
        items = items.exclude(invoice__type__in=exclude_types)

    items = items.order_by('invoice__created')

    rates = ExchangeRates.objects.get()

    for i in items:
        i.set_rates(rates)

    return items


def _get_invoice_totals(items):
    return {
        'qty': sum([i.qty for i in items]),
        'wholesale_total': sum([i.wholesale_subtotal_uah for i in items]),
        'retail_total': sum([i.subtotal_with_discount for i in items]),
        'discounted_retail_total': sum([i.discounted_subtotal for i in items]),
        'profit_total': sum([i.profit_subtotal_uah for i in items])
    }


def _get_invoice_model(invoice_type):

    models = {
        'sale': Sale,
        'arrival': Arrival
    }

    try:
        return models[invoice_type]
    except KeyError:
        pass

    raise Exception('Unknown invoice type: {}'.format(invoice_type))


def _get_invoice_item_model(invoice_type):

    models = {
        'sale': SaleItem,
        'arrival': ArrivalItem
    }

    try:
        return models[invoice_type]
    except KeyError:
        pass

    raise Exception('Unknown invoice type: {}'.format(invoice_type))


def _get_invoice(invoice_type, invoice_id):
    return get_object_or_404(_get_invoice_model(invoice_type), pk=invoice_id)
