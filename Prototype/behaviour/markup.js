/*!
 * (Intelligent) markup handling
 *
 * Copyright 2008, 2009 Simplon
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
var idcount = 0;

function assertId(el) {
    el = $(el);
    var id = el.attr("id");

    if (!id) {
        idcount+=1;
        id="id"+String(idcount);
        el.attr("id", id);
    }
    return id;
}


function setupSuperimpose() {
    var label = this,
        forInput = $(label).attr("for"),
        myInput = forInput ? $("#"+forInput) : $(":input", label);
    if (forInput && !myInput.length) {
        myInput = $(":input[name=" + forInput + "]");
    }
    if (!myInput.length) {
        return;
    }

    $(label)
        .css("display", $(myInput).val()==="" ? "block" : "none")
        .click(function() {
            $(myInput).focus();
        });

    // Check after a little bit to test if a browser silently entered
    // form data after DOM load. Safari 4 needs this.
    setTimeout(function() {
        $(label).css("display", $(myInput).val()==="" ? "block" : "none");
        }, 250);

    $(myInput)
        .unbind(".superimpose");

    $(myInput)
        .bind("blur.superimpose", function(e) {
            $(label).css("display", $(myInput).val()==="" ? "block" : "none");
        })
        .bind("focus.superimpose", function(e) {
            $(label).css("display", "none");
        });
}

// Check if all dependenceis as spcified in `dependsOn` classes for
// an element are satisfied.
function verifyDependencies(slave) {
    var $el = $(slave),
        classes = $el.attr("class").split(" "),
        $input, i, value, parts; 

    for (i=0; i<classes.length; i++) {
        parts = classes[i].split("-");
        if (parts.length<2 || parts[0]!=="dependsOn") {
            continue;
        }

        $input = $(":input[name="+parts[1]+"]");
        if (!$input.length) {
            return false;
        }

        if ($input.attr("type")==="radio" || $input.attr("type")==="checkbox") {
            value = $input.filter(":checked").val();
        } else {
            value = $input.val();
        }

        if ((parts.length===2 || parts[2]==="on") && !value) {
            return false;
        } else if (parts[2]==="off" && value) {
            return false;
        } else if (parts.length>3) {
            if (parts[2]==="equals" && parts[3]!==value) {
                return false;
            } else if (parts[2]==="notEquals" && parts[3]===value) {
                return false;
            }
        } 
    }

    return true;
}


// Return the list of all input elements on which the given element has
// a declared dependency via `dependsOn` classes.
function getDependMasters(el) {
    var $classes = $(el).attr("class").split(" "),
        $result = $(),
        i, parts;

    for (i=0; i<$classes.length; i++) {
        parts = $classes[i].split("-");
        if (parts.length<2 || parts[0]!=="dependsOn") {
            continue;
        }

        $result=$result.add(":input[name="+parts[1]+"]");
    }

    return $result;
}


// Setup dependency-tracking behaviour.
function initDepends(root) {
    $("*[class*='dependsOn-']", root).each(function() {
        var $slave = $(this);

        if (verifyDependencies($slave)) {
            $slave.show();
        } else {
            $slave.hide();
        }

        getDependMasters($slave).bind("change.depends", function() {
            if (verifyDependencies($slave)) {
                $slave.slideDown();
            } else {
                $slave.slideUp();
            }
        });
    });
}


// Animation function for fancy effect when showing a BeautyTips
// tooltip. Use as the showTip option.
function BeautyTipShow(box) {
    var $content = $('.bt-content', box).hide(); /* hide the content until after the animation */
    var $canvas = $('canvas', box).hide(); /* hide the canvas for a moment */
    var origWidth = $canvas[0].width; /* jQuery's .width() doesn't work on canvas element */
    var origHeight = $canvas[0].height;
    $(box).show(); /* show the wrapper, however elements inside (canvas, content) are now hidden */
    $canvas
      .css({width: origWidth * 0.5,
            height: origHeight * 0.5,
            left: origWidth * 0.25,
            top: origHeight * 0.25,
            opacity: 0.1})
      .show()
      .animate({width: origWidth,
                height: origHeight,
                left: 0,
                top: 0,
                opacity: 1},
                400, 'easeOutBounce',
                function(){
                    $content.show();} /* show the content when animation is done */
                );
}

// Animation function for fancy effect when hiding a BeautyTips
// tooltip. Use as the hideTip option
function BeautyTipHide(box, callback) {
    $('.bt-content', box).hide();
    var $canvas = $('canvas', box);
    if ($canvas.length===0) { return; }
    var origWidth = $canvas[0].width;
    var origHeight = $canvas[0].height;
    $canvas
      .animate({width: origWidth * 0.5,
                height: origHeight * 0.5,
                left: origWidth * 0.25,
                top: origHeight * 0.25,
                opacity: 0
                },
                400, 'swing', callback);
}


jQuery.fn.toolTip = function(content, options) {
    var postShow = function(box) {
        var tipsource = $(this);
        var monitor = tipsource.add($(box));
        var timer;

        tipsource.data("btdelay.hover", true).data("btdelay.delay", 0);

        var checkRemove = function() {
            var hovered = tipsource.data("btdelay.hover");

            if (hovered) {
                tipsource.data("btdelay.delay", 0);
            } else {
                var delay = tipsource.data("btdelay.delay");
                if (delay<5) {
                    tipsource.data("btdelay.delay", delay+1);
                } else {
                    clearInterval(timer);
                    monitor.unbind(".btdelay");
                    tipsource.btOff();
                }
            }
        };

        monitor.bind("mouseenter.btdelay", function() { tipsource.data("btdelay.hover", true); })
               .bind("mouseleave.btdelay", function() { tipsource.data("btdelay.hover", false); });
        timer=setInterval(checkRemove, 100);
    };

    var opt = (typeof content == "string") ? options : content;
    opt = jQuery.extend(opt, {trigger: "none", postShow: postShow});

    return this.each(function(index) {
        var hoverOpts = {
                over : function() {
                           if (!$(this).data("btdelay.hover")) {
                               $(this).btOn();
                           }
                       },
                out : function() { }
                };
    
        $(this).bt(content, opt).hoverIntent(hoverOpts);
    });
};


// Set some default styles for BeautyTip
jQuery.bt.options.positions="top, right, left, bottom";
jQuery.bt.options.showTip=BeautyTipShow;
jQuery.bt.options.hideTip=BeautyTipHide;
jQuery.bt.options.fill="#c16800";
jQuery.bt.options.cornerRadius=0;
jQuery.bt.options.strokeWidth=1;
jQuery.bt.options.strokeStyle="#f6921d"; 
jQuery.bt.options.shadow=true;
jQuery.bt.options.shadowOffsetX=0;
jQuery.bt.options.shadowOffsetY=0;
jQuery.bt.options.shadowBlur=5;
jQuery.bt.options.spikeLength= 10; 
jQuery.bt.options.spikeGirth= 10;
jQuery.bt.options.padding= 10;
// jQuery.bt.options.cssStyles={
//         fontFamily: '"lucida grande",tahoma,verdana,arial,sans-serif', 
// 		fontSize: '13px',
//         "line-height": '20px',
// 		color: 'white'
//   };
jQuery.bt.options.shadowColor="rgba(0,0,0,.6)";
jQuery.bt.options.shadowOverlap=false;
jQuery.bt.options.noShadowOpts={strokeStyle: "white",
                                strokeWidth: 2
                                };



$(".printButton").live("click", function() {
    window.print();
    return false;
});


$(document).ready(function() {
    $(".jsOnly").show();

    var tmp;

    // Automatically setup accordions
    $(".accordion").accordion();

    // Numeric input fields
    $("input.numeric").numeric();

    // Turn legend into p.question. Workaround for browsers which can not
    // style legend elements.
    $("legend").each(function() {
        $(this).replaceWith('<p class="question">'+$(this).html()+'</p>');
    });

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

    // Show/hide labels for input elements depending on their contents.
    $("label.superImpose").each(setupSuperimpose);

    initDepends(document);

    // Set selected and hover attributes on checkboxes and radio buttons.
    // Allows for more flexible styling.
    $("ul.radioList,ul.radioRow").each(function() {
        var list = $(this);

        list.find("li input")
            .hover(
                function() { $(this).parents("li").addClass("hover"); },
                function() { $(this).parents("li").removeClass("hover"); })
            .click(function() {
                list.find("li").removeClass("selected");
                list.find("li input:checked").parents("li").addClass("selected");
            });

        $("li input:checked", list).parents("li").addClass("selected");
    });

    function setSelectForCheckbox(el) {
        var label = $(el).parents("label");
        if (el.checked) {
            $(label).addClass("selected");
        } else {
            $(label).removeClass("selected");
        }
    }

    $("label input[type=checkbox]")
        .click(function() { setSelectForCheckbox(this); })
        .each(function() { setSelectForCheckbox(this); });

    if (!(engine==="msie" && engine_version<70)) {
        // Title attributes get an on-hover tooltip 
        $("*[title][rel!=fancybox]:not(form):not('.clicktip')").toolTip({shrinkToFit: true});
    }
    if (engine==="msie" && engine_version<80) {
        $(".clicktip").each(function() { 
            $(this).click(function() { return false; });
        });
    }
    else {
        // Clicktips are activated by clicking on an item
        $(".clicktip").each(function() {
            var id = assertId(this);
            $(this).bt({trigger: "click",
                        fill: "#8293ab",
                        strokeStyle: "#8293ab", 
                        contentSelector: "$('#" + id + "').html()"
                        })
                .click(function() { return false; });
        });
    }

    $(".focustip").each(function() {
	var target = $(this).attr("class").match(/target-id-([A-Za-z0-9_\-]+)/);
	if (target) {
            var id = assertId(this);
            $("#"+target[1]).bt({
                trigger: ["focus", "blur"],
                contentSelector: "$('#" + id + "').html()"
            });
        }
    });

    tmp = $(".autofocus:first");
    if (tmp.length) {
        tmp.get(0).focus();
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

/*jslint browser: true, undef: true, nomen: true, eqeqeq: true, bitwise: true, regexp: true, newcap: true, immed: true */
