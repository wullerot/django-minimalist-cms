(function($) {

    $.widget( "minimalist_cms.edit_item", {

        options: {
            _: "_"
        },

        iframe_link: null,

        _create: function() {
            this.my_iframe_link = this.element.attr('href');
            this.toolbar = $('.minimalist-cms-toolbar').data('minimalist_cms-cms_toolbar');
            this._on(this.element, {'click': this.on_edit_click});
        },

        on_edit_click: function(e) {
            e.preventDefault();
            this.toolbar.open_iframe(this.iframe_link);
        },

        _destroy: function(e) {

        },

    });
})($);
