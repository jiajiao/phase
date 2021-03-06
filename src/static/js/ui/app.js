var Phase = Phase || {};

jQuery(function($) {
    "use strict";

    var dispatcher = Phase.Events.dispatcher;

    var toggleButtons = $('.toggle-content-button');
    toggleButtons.each(function(counter, button) {
        new Phase.Views.ToggleContentButton({ el: button });
    });

    var modalView = new Phase.Views.ModalView();

    var auditModalView = new Phase.Views.AuditModalView();

    var actionMenus = $('ul.action-menu');
    actionMenus.each(function(counter, menu) {
        new Phase.Views.ActionMenuView({ el: menu });
    });

    $(document).keyup(function(event) {
        if (event.keyCode === 27) {
            dispatcher.trigger('onEscKeyPressed');
        }
    });
});
