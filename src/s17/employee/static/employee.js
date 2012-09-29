(function ($) {

    $('.portaltype-employee .portalMessage a[href$="@@new-user"]').prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: 'form.kssattr-formname-new-user',
        noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
        redirect: function () {return location.href;}
    });

    $('#employee-image').prepOverlay({
         subtype: 'image',
         urlmatch: '/image_.+$',
         urlreplace: ''
    });

})(jQuery);
