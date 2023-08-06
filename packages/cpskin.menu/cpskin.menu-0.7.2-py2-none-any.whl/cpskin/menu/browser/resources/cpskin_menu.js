$( document ).ready(function() {

    var clickable_menu_selector = '#portal-globalnav li:not(#portaltab-index_html) a';
    $(clickable_menu_selector).each(function(){
        $(this).parent('li').attr('aria-expanded', 'False');

        var set_focus = function(element) {
          element.get(0).focus();
        };

        var deactivate_listeners = function(submenu) {
          $(submenu).find('.firstitem a').off('keydown');
          $(submenu).find('.lastItem a').off('keydown');
        };

        var detect_go_back = function(element) {
          $(element).on('keydown', function(e) {
            // Shift + Tab
            if (e.shiftKey && e.keyCode == 9) {
              e.preventDefault();
              back_to_level1(element);
            }
            // Up arrow
            if (e.keyCode == 38) {
              e.preventDefault();
              back_to_level1(element);
            }
          });
        };

        var detect_go_next = function(element) {
          $(element).on('keydown', function(e) {
            // Shift + Tab
            if (e.keyCode == 9) {
              e.preventDefault();
              go_to_next_level1(element);
            }
            // Down arrow
            if (e.keyCode == 40) {
              e.preventDefault();
              go_to_next_level1(element);
            }
          });
        };

        var get_level_entry = function(element) {
          if ($(element).attr('id') && $(element).attr('id').startsWith('portal-globalnav-cpskinmenu')) {
            return $(element);
          } else {
            return $(element).closest('.portal-globalnav-cpskinmenu.navTreeLevel0');
          }
        };

        var back_to_level1 = function(element) {
          var submenu = get_level_entry(element);
          var menu_id = '#' + submenu.attr('id').replace('-globalnav-cpskinmenu-', 'tab-') + " a";
          $(menu_id).click();
          set_focus($(menu_id));
          deactivate_listeners(submenu);
        };

        var go_to_next_level1 = function(element) {
          var submenu = get_level_entry(element);
          var menu_id = '#' + submenu.attr('id').replace('-globalnav-cpskinmenu-', 'tab-') + " a";
          $(menu_id).click();
          set_focus($(menu_id).parent().next().children('a'));
          deactivate_listeners(submenu);
        };

        $(this).click(function() {
            var activated = $(this).hasClass('activated');
            var menu_id = this.parentNode.id.replace('portaltab-', '');
            var submenu_id = '#portal-globalnav-cpskinmenu-' + menu_id;

            if (!activated) {
                $(this).parent('li').attr('aria-expanded', 'True');
                $(clickable_menu_selector).each(function(){
                    $(this).removeClass('activated');
                    $(this).parent('li').removeClass('menu-activated');
                });
                $(this).addClass('activated');
                $(this).parent('li').addClass('menu-activated');

                $('ul.sf-menu').each(function(){
                    $(this).hide();
                });
                $(submenu_id).show();
                set_focus($(submenu_id + " .firstItem a").first());
                $(submenu_id + " .firstItem").attr('aria-expanded', 'True');
                detect_go_back($(submenu_id + " .firstItem a").first());
                detect_go_next($(submenu_id + " .lastItem a").last());
            } else {
                $(this).removeClass('activated');
                $(this).parent('li').removeClass('menu-activated');
                $(this).parent('li').attr('aria-expanded', 'False');
                $(submenu_id).hide();
            }
            return false;
        })
    });

});
