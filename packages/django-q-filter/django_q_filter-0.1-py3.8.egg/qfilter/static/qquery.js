//
// Make Quick Filters selectable
//

$(document).ready(function () {
    $('#quick-filters-modal select').select2();
    $('#quick-filters-list select').select2();

    // Add selected quick filter to input field
    $('#quick-filters-modal select').on('change', function (e) {
        $('input[name=qfilter]').val(this.options[this.selectedIndex].value);
        $('#qfilter-tab-query-nav').tab('show')
    });

    // Redirect to Quick Filter on select
    $('#quick-filters-list select').on('change', function (e) {
        window.location.href = this.options[this.selectedIndex].value
    });

    //
    // Q Query Wizard
    //
    
    $('#qfilter-wizard-multi-form .form-container').formset({
        formTemplate: '#qfilter-wizard-form-empty',
        addText: '<i class="fas fa-plus"></i> Add Filter',
        addContainerClass: 'qfilter-wizard-multi-form-add-more',
        addFormContainerClass: 'dynamic-form-add',
        addCssClass: 'add-row btn btn-default mb-0',
        deleteText: '<i class="fas fa-times"></i>',
        deleteContainerClass: 'delete-row',
        deleteCssClass: 'delete-row btn btn-block btn-default m-0 p-2 d-flex flex-sm-column align-items-center justify-content-left justify-content-sm-center'
    });

    // select2-ify dropdowns
    $('#qfilter-wizard-multi-form select').select2();
    $('#qfilter-wizard-multi-form .add-row').click(function() {
        $('#qfilter-wizard-multi-form select').select2();
    });
});