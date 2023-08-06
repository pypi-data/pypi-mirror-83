$( document ).ready(function() {

    // Click outside of the menu
    $(document).click(function(event) {
        if(!$(event.target).closest('ul.sf-menu').length) {
            hide_superfish_submenu();
        }
    });

    hide_superfish_submenu = function()
    {
        if($('ul.sf-menu').is(":visible")) {
            $('ul.sf-menu').each(function(){
                $(this).hide();
            });
        }
    }
    hide_superfish_submenu();
});