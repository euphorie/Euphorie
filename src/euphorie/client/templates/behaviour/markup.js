/*!
 * (Intelligent) markup handling
 *
 * Copyright 2008-2013 Simplon B.V.
 */

(function($) {
        var is_href_internal = new RegExp("^https?://"+window.location.host, "i");

        $(".jsOnly").show();

        $(".printButton").on("click", function() {
            window.print();
            return false;
        });

        $("input.numeric,input[type=number]").numeric();


        $("a[rel=fancybox]").fancybox({
            "transitionIn"    : "elastic",
            "transitionOut"   : "elastic",
            "titlePosition"   : "over"
        });

        $("a[rel=download]").click(function(e) {
            if (typeof _gaq==="object") {
                var href = e.target.href,
                    path = href.replace(new RegExp("https?://" + location.host + "/", "i"), "/");
                 _gaq.push(["_trackPageview", path]);
            }
        });

        $("a").click(function() {
            if (typeof _gaq!=="object")
                return;
            if (is_href_internal.test(event.target.href))
                return;
            _gaq.push(["_trackEvent", "external-link", "click", event.target.href]);
        });

        if ($.browser.msie) {
            var browser_version = Number($.browser.version.split(".", 1)[0]);
            // PNG transparancy fix for MS Internet Explorer 6
            if (browser_version<7) {
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

            // Work around broken button behaviour for IE 6 and 7
            if (browser_version<8) {
                $("form button[type=submit]").on("click", function() {
                    var name = $(this).attr("name"),
                        value = $(this).attr("class").split(" ")[0];

                    $("<input type='hidden'/>")
                        .attr("name", name)
                        .attr("value", value)
                        .appendTo(this.form);
                    $("button[type=submit]", this.form).attr("name", "_buttonfix");
                });
            }
        }

        // iPhone hackery
        if (navigator.userAgent.search("iPhone")!==-1) {
            setTimeout(function() {
                    window.scrollTo(0, 1);
                }, 100);
        }
})(jQuery);
