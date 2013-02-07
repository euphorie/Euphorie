/*!
 * (Intelligent) markup handling
 *
 * Copyright 2008-2013 Simplon B.V.
 */

function GetBrowserVersion() {
    return Number( $.browser.version.split(".", 2).join(""));
}

function GetBrowserEngine() {
    var i, engines = [ "safari", "opera", "msie", "mozilla" ];
    for (i=0; i<engines.length; i++) {
        if ($.browser[engines[i]]) {
            return engines[i];
        }
    }
}

var engine = GetBrowserEngine();
var engine_version = GetBrowserVersion();
var iphone = (navigator.userAgent.search("iPhone")!==-1);


$(".printButton").on("click", function() {
    window.print();
    return false;
});


$(document).ready(function() {
    $(".jsOnly").show();

    var tmp;

    // Numeric input fields
    $("input.numeric").numeric();

    // PNG transparancy fix for MS Internet Explorer 6
    if (engine==="msie" && engine_version<70) {
        var fixImage = function(img) {
            $(img).css({
                    height: "0px",
                    width: $(img).width()+"px",
                    "padding-top" : $(img) .height()+"px",
                    overflow : "hidden",
                    filter : "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + $(img).attr("src") + "', sizingMethod='image')"
                    });
        };

        $("img[src$=.png]").each(function() {
            fixImage(this);
        });
    }

    $("a[rel=fancybox]").fancybox({
            "transitionIn"    : "elastic",
            "transitionOut"   : "elastic",
            "titlePosition"   : "over"
            });

});


// Work around broken button behaviour for IE 6 and 7
if (engine==="msie" && engine_version<80) {
    $("form button[type=submit]").live("click", function() {
        var name = $(this).attr("name"),
            value = $(this).attr("class").split(" ")[0];

        $("<input type='hidden'/>")
            .attr("name", name)
            .attr("value", value)
            .appendTo(this.form);
        $("button[type=submit]", this.form).attr("name", "_buttonfix");
    });
}

// iPhone hackey
if (iphone) {
    var updateLayout = function() {
        window.scrollTo(0, 1);
    };

    $(document).ready(function() {
        setTimeout(updateLayout, 100);
    });
}

