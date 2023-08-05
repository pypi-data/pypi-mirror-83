
SelectServiceItemList = function (params) {

    var $container = params.$container;

    function handleListItemDoubleClick() {
        $(window).trigger('service-selected', [$(this).data('item-id')]);
    }

    $container.on('dblclick', '[data-role=list-item]', handleListItemDoubleClick);

};
