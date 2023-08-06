"use strict";
var KTLayout = function() {
    var body;

    var header;
    var headerMenu;
    var headerMenuOffcanvas;
    var mobileHeaderTopbarToggle;

    var asideMenu;
    var asideMenuOffcanvas;

    var scrollTop;

    var pageStickyPortlet;

    // Header
    var initHeader = function() {
        var tmp;
        var headerEl = KTUtil.get('kt_header');
        var options = {
            classic: {
                desktop: true,
                mobile: false
            },
            offset: {},
            minimize: {}
        };

        options.minimize.mobile = false;

        if (KTUtil.attr(headerEl, 'data-ktheader-minimize') == 'on') {
            options.minimize.desktop = {};
            options.minimize.desktop.on = 'kt-header--minimize';
            options.offset.desktop = parseInt(KTUtil.css(headerEl, 'height')) - 10;
        } else {
            options.minimize.desktop = false;
        }

        header = new KTHeader('kt_header', options);

        if (asideMenu) {
            header.on('minimizeOn', function() {
                asideMenu.scrollReInit();
            });

            header.on('minimizeOff', function() {
                asideMenu.scrollReInit();
            });
        }        
    }

    // Header Menu
    var initHeaderMenu = function() {
        // init aside left offcanvas
        headerMenuOffcanvas = new KTOffcanvas('kt_header_menu_wrapper', {
            overlay: true,
            baseClass: 'kt-header-menu-wrapper',
            closeBy: 'kt_header_menu_mobile_close_btn',
            toggleBy: {
                target: 'kt_header_mobile_toggler',
                state: 'kt-header-mobile__toolbar-toggler--active'
            }
        });

        headerMenu = new KTMenu('kt_header_menu', {
            submenu: {
                desktop: 'dropdown',
                tablet: 'accordion',
                mobile: 'accordion'
            },
            accordion: {
                slideSpeed: 200, // accordion toggle slide speed in milliseconds
                expandAll: false // allow having multiple expanded accordions in the menu
            }
        });
    }

    // Header Topbar
    var initHeaderTopbar = function() {
        mobileHeaderTopbarToggle = new KTToggle('kt_header_mobile_topbar_toggler', {
            target: 'body',
            targetState: 'kt-header__topbar--mobile-on',
            togglerState: 'kt-header-mobile__toolbar-topbar-toggler--active'
        });
    }

    return {
        init: function() {
            body = KTUtil.get('body');
            this.initHeader();
        },

        initHeader: function() {
            initHeader();
            initHeaderMenu();
            initHeaderTopbar();
        },
    };
}();

// webpack support
if (typeof module !== 'undefined') {
    module.exports = KTLayout;
}

// Init on page load completed
KTUtil.ready(function() {
    KTLayout.init();
});