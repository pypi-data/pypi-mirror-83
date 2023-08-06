/* initialise plugins */
;(function($){
    "use strict";

    var FL_PREFIX = 'first-level-';
    var SUBMENU_PREFIX = 'advb-submenu-level-';
    var ADVB_TITLE_PREFIX = 'title-level-';

    function update_element_id($elements, PREFIX){
         $elements.each(function(index, value){
            var element = $(value);
            var new_id = PREFIX + element.attr('id');
            element.attr('id', new_id);
        })
    }

    function extract_submenu_children($elements, level, createdby){
        var $new_ul = $("<ul class='submenu submenu-level-" + level + "' />");
        $elements.children('li').each(function(index, value){
            var $children = $(this).find('> ul');
            var $new_li = $("<li />");
            var li_class = $children.length > 0 ? 'nofollow' : 'follow';
            var selected = '';
            if ($(this).find('> span').hasClass('selected')){
                selected = 'selected';
            }
            $new_li.addClass(li_class)
                   .addClass(selected)
                   .text($(this).find('> span > a').text().trim())
                   .data('referto', $(this).attr('id'))
                   .data('level', level)
                   .data('orig_id', $(this).attr('id'));

            //if we have link or level is greater than 1 follow the link
            if(li_class=='follow' || level > 3){
                //we don't have children or we are in a level where we should follow the link
                $new_li.data('follow', $(this).find('span a').attr('href'));
                $new_li.on('click', function(){
                   location.href =  $(this).data('follow');
                });
            }
            else{
                  // we have children and we need to open it in a new level menu
                  $new_li.on('click', function(){
                      //var orig =  $('#'+$(this).data('referto').replace('.', '\\.'));
                      var orig = $('#'+$(this).data('referto').replace( /(:|\.|\[|\])/g, "\\$1" ))
                      //remove all the collapsible siblings: next levels
                      //but let's prevent to remove nextMenu if we select an already opened
                      var orig_id = $(this).data('orig_id');
                      var remove = true;

                      // check if we already have this menu in breadcrumbs
                      var $others_menu = $(this).parent().parent().nextAll();
                      $others_menu.each(function(){
                          if ($(this).data('orig_id') == orig_id)
                              remove = false;
                              return false;
                      })
                      // in any case, collapse the actual menu
                      $(this).parent().prev().click();
                      //if not, remove all next menu and update breadcrumbs if yes open correct menu
                      if (remove){
                          $(this).parent().parent().nextAll().remove();
                          //create new levels
                          $('#advanced-breadcrumbs').append(create_menu_level(orig, $(this).data('level')+1, 'click'));}
                      else{
                          //need to open the next menu
                          $others_menu.each(function(){
                              if ($(this).data('orig_id') == orig_id)
                                  $(this).show().find('> span').click();
                          })
                      }
                  });
            }
            $new_ul.append($new_li);
        });
        if (createdby  == 'click')
            $new_ul.css({'display':'block'}).addClass('submenu-active');
        return $new_ul.children().length > 0 ? $new_ul : '';
    }

    function create_menu_level($element, level, createdby){
        var $new_level = $("<div class='advb-submenu' id='" + SUBMENU_PREFIX + level + "'/>")
                         .data('orig_id', $element.attr('id'));
        var $childrens = $element.find('> ul');
        //at most 5 level
        if (level<5){
            var selected = '';
            if ($element.find('> span').hasClass('selected')){
                selected = 'selected';
            }
            var $title = $("<span class='advb-title' id='" + ADVB_TITLE_PREFIX  + level +"' />")
                  .addClass(selected)
                  .append($.trim($element.find('> span a').text()))
                  .on('click',
                      function(){
                          //open correct menu and close the others
                          toggle_menu($(this).parent().find('> ul'));
                      });
            $new_level.append($title);
            $new_level.append(extract_submenu_children($childrens, level, createdby));
            return $new_level;
            }
        return '';
    }

    function hide_opened_menus(){
        $('#advanced-breadcrumbs').children().children('ul').slideUp().removeClass('submenu-active');
    }

    function toggle_menu($submenu) {
        if (!$submenu.hasClass('submenu-active')) {
            hide_opened_menus();
        }
        $submenu.slideToggle() .toggleClass('submenu-active');
    }

    function create_breadcrumb($menu){
        /*
         * read from the menu structure le selected elements path and build collapsible breadcrumbs
         * */
        var $cloned_menu = $('<div />').append($menu.clone());
        $breadcrumbs = $().add($cloned_menu).add($menu.find('.navTreeItemInPath'));
        //add selected element to bc only if it's a list
        if($menu.find('.selected').parent().find('> ul').length > 0){
            var $breadcrumbs = $breadcrumbs.add($menu.find('.selected').parent());
        }
        //get all the li elements in the path and create the menu
        $($breadcrumbs).each(function(index, value){
                var element = $(value);
                $('#advanced-breadcrumbs').append(create_menu_level(element, index+1, 'breadcrumbs'));
        })
        $('#advanced-breadcrumbs').find('div ul').hide();
        $('#advanced-breadcrumbs').find('#title-level-1').hide();
        $('#advanced-breadcrumbs').find('.advb-submenu').filter(function(index){return index!==0}).hide();
    }

    function setupInPathAndSelectedItems() {
        var isSelectedLeaf = function(el) {
            var href = $(el).attr('href'); 
            return location.href == href;
        }

        var isInPath = function(el) {
            var href = $(el).attr('href'); 
            return location.href.indexOf(href) > -1;
        }

        $('.portal-globalnav-cpskinmenu li span a').filter(function() {
                return isSelectedLeaf(this);
        }).parent().addClass("selected");
        //$('.cpskinmenu-load-page > li > span > a').filter(function() {
        //        return isInPath(this);
        //}).parent().parent().parent().show();
        $('.portal-globalnav-cpskinmenu li span a').filter(function() {
                return isInPath(this) && !isSelectedLeaf(this);
        }).parent().parent().addClass("navTreeItemInPath");
        //$('.portal-globalnav-cpskinmenu.sf-menu').find('.navTreeItemInPath').parent().show();
        //$('.portal-globalnav-cpskinmenu.sf-menu').find('.selected').parent().parent().show();
    }

    $( document ).ready(function() {
        setupInPathAndSelectedItems();

        //initialize superfish
        $('ul.sf-menu').superfish({
          onShow: function() {
            var entry = $(this).parent('li');
            if (entry) {
              entry.attr('aria-expanded', 'True');
            }
          },
          onHide: function() {
            var entry = $(this).parent('li');
            if (entry) {
              entry.attr('aria-expanded', 'False');
            }
          },
        });

        //initialize drop down menu
        var $menu = $('#portal-globalnav-cpskinmenu-mobile');
        $('#mobnav-btn').on('click',
           function(){
               toggle_menu($('#advanced-breadcrumbs .submenu-level-1'));
           });

        create_breadcrumb($menu);

        $('#search-btn').click(function(e){
          e.preventDefault();
          $(this).toggleClass('selected');
          $('#portal-searchbox').toggle();
          $('#portal-searchbox input.searchField').focus();
        });
    });
})(jQuery);
