$(document).ready(function () {

    $("a#oira_legal_hide_anchor").click(function(event) {
        event.preventDefault();
        jQuery("a#oira_legal_hide_anchor").hide();
        jQuery("a#oira_legal_show_anchor").show();
        jQuery("div#legal_reference").show(200);
    });

    $("a#oira_legal_show_anchor").click(function(event) {
        event.preventDefault();
        jQuery("a#oira_legal_hide_anchor").show();
        jQuery("a#oira_legal_show_anchor").hide();
        jQuery("div#legal_reference").hide(200);
    });
});
