$(document).ready(function () {
    var fadeOut = function() { $("a#standardSolutionsLink").css("background-image", "None"); };
    var fadeIn = function() { $("a#standardSolutionsLink").css("background-image", "url(++resource++euphorie.style/button-default.png)"); };
    var toggleFade = function() {
        fadeOut();
        setTimeout(function() { fadeIn(); }, 300);
    };

    $("a#standardSolutionsLink").ready(function () {
        setTimeout( function () { toggleFade(); }, 1000);
        setTimeout( function () { toggleFade(); }, 2000);
        setTimeout( function () { toggleFade(); }, 3000);
        }
    );

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
