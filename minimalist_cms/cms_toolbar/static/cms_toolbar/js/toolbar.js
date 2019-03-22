(function($) {
    $.widget( "minimalist_cms.cms_toolbar", {

        options: {
            // 'menu': [],
            _: "_"
        },

        narrow_class: 'minimalist-cms-overlay_narrow',
        wide_class: 'minimalist-cms-overlay_wide',

        $iframe: null,
        $close: null,
        $handle: null,
        $overlay: null,
        $content: null,
        $btn_edit: null,
        $btn_hide_overlay: null,
        $content_buttons: null,
        $btn_logout: null,

        _create: function() {
            // find various elements
            this.auth_status = this.element.attr('data-auth');
            this.$overlay_background = $('.minimalist-cms-overlay-background');
            this.$overlay = this.element.find('[data-id="overlay"]');
            this.$content = this.element.find('[data-id="content"]');
            this.$content_list = this.$content.find('> div');
            this.$iframe_wrap = this.$overlay.find('[data-id="iframe"]');
            this.$iframe = this.$iframe_wrap.find('iframe');
            this.$handle = this.element.find('[data-id="handle"]');
            this.$btn_edit = this.element.find('[data-id="btn-edit"]');
            this.$btn_hide_overlay = this.element.find('[data-id="btn-hide-overlay"]');
            this.$btn_logout = this.element.find('[data-id="btn-logout"]');
            this.$content_buttons = this.element.find('[data-content]');

            // add handlers for toolbar items
            this._on(this.$content_buttons, {'click': this.open_content});
            this._on(this.$btn_hide_overlay, {'click': this.close_modal});
            this._on(this.$btn_logout, {'click': this.on_logout});
            this._on(this.$content.find('a'), {'click': this.on_content_link});
            this._on(this.$overlay_background, {'click': this.close_modal});
            this._on($(window), {'keyup': this.check_esc_close});

            // iframe
            this._on(this.$iframe, {'load': this.on_iframe_load});

            // add edit buttons
            $('.minimalist-cms-edit-link').edit_item();

            // some init

        },

        on_logout: function(e) {
            this.element.delay(400).fadeOut(100, function() {
                document.location.href = '/';
            })
        },

        on_content_link: function(e) {
            e.preventDefault();
            let $a = $(e.currentTarget);
            let target_url = $a.attr('href');
            let narrow = $a.attr('data-narrow');
            this.open_iframe(target_url, narrow);
        },

        open_iframe: function(target_url, narrow=false) {
            this.hide_content();
            this.$iframe_wrap.show(0);
            this.$iframe.attr('src', target_url);
            this.$iframe.css('opacity', 0);
            this.open_modal(narrow);
        },

        on_iframe_load: function(e) {
            // scrollbar: always!
            this.$iframe.contents().find('body').css('overflow-y', 'scroll');
            // this.$iframe.contents().find('body').css('overflow-x', 'auto');
            // header: remove
            this.$iframe.contents().find('#header').remove();
            // breadcrumbs: remove
            this.$iframe.contents().find('.breadcrumbs').remove();
            // view on site: target=_top!
            this.$iframe.contents().find('.viewsitelink').attr('target', '_top');
            // ready?!
            this.$iframe.show(0);
            this.$iframe.css('opacity', 1);
            // prepare for next page load!
            // https://stackoverflow.com/questions/17315013/detect-when-an-iframe-starts-to-load-new-url
            this._on(this.$iframe[0].contentWindow, {'unload': this.onunload_iframe});

        },

        onunload_iframe: function(e) {
            this.$iframe.css('opacity', 0);
        },

        hide_iframe: function() {
            this.$iframe_wrap.hide(0);
            this.$iframe.removeAttr('src');
            this.$btn_hide_overlay.hide(0);
        },

        open_content: function(e) {
            e.preventDefault();
            this.hide_iframe();
            let $a = $(e.currentTarget);
            let target_content = $a.attr('data-content');
            this.$content_list.hide(0);
            this.$content.show(0);
            this.$content_list.filter('[data-id="content-' + target_content + '"]').show(0);
            this.open_modal(true);
        },

        hide_content: function() {
            this.$content_list.hide(0);
            this.$content.hide(0);
        },

        check_esc_close: function(e) {
            if (e.keyCode == 27) {  // esc
                this.close_modal();
            }
        },

        close_modal: function() {
            if (this.$overlay_background.is(':visible')) {
                this.$overlay_background.fadeOut(100);
                this.$btn_hide_overlay.hide(0);
                this.$overlay.removeClass(this.wide_class);
                this.$overlay.removeClass(this.narrow_class);
                document.location.reload();
            }
        },

        open_modal: function(narrow) {
            this.$overlay_background.fadeIn(100);
            this.$btn_hide_overlay.show(0);
            if (narrow) {
                this.narrow_modal();
            } else {
                this.widen_modal();
            }
        },

        narrow_modal: function() {
            this.$overlay.addClass(this.narrow_class);
            this.$overlay.removeClass(this.wide_class);
        },

        widen_modal: function() {
            this.$overlay.addClass(this.wide_class);
            this.$overlay.removeClass(this.narrow_class);
        },

        _destroy: function(e) {

        },

    });
})($);
