
CustomerSelect = function (params) {

    var $field = params.$field,
        url = params.url;

    $field.select2({
        language: 'uk'
    });

    function handleFieldChange() {
        var customerId = $(this).val(),
            data = {customer: customerId};

        $field.prop('disabled', true);

        $.post(url, data, handleCustomerSet);
    }

    function handleCustomerSet(response) {
        $field.prop('disabled', false);
        $.notify({message: response.message}, {type: 'success'});
        $(window).trigger('product-total-updated', response.total);
    }

    $field.on('change', handleFieldChange);

};
