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

        $input = $(":input[name='"+parts[1]+"']");
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

        $result=$result.add(":input[name='"+parts[1]+"']");
    }

    return $result;
}


function initPlaceHolders(root) {
    // check placeholder browser support
    if (!Modernizr.input.placeholder) {
        // set placeholder values
        $(root).find('[placeholder]').each(function() {
            if ($(this).val() === '') { // if field is empty
                $(this).val( $(this).attr('placeholder') );
            }
        });
		
        // focus and blur of placeholders
        $('[placeholder]', root).focus(function() {
            if ($(this).val() === $(this).attr('placeholder')) {
                $(this).val('');
                $(this).removeClass('placeholder');
            }
        }).blur(function() {
            if ($(this).val() === '' || $(this).val() === $(this).attr('placeholder')) {
                $(this).val($(this).attr('placeholder'));
                $(this).addClass('placeholder');
            }
        });
		
        // remove placeholders on submit
        $('[placeholder]', root).closest('form').submit(function() {
            $(this).find('[placeholder]').each(function() {
                if ($(this).val() === $(this).attr('placeholder')) {
                    $(this).val('');
                }
            });
        });
    }
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



$(".printButton").live("click", function() {
    window.print();
    return false;
});


$(document).ready(function() {
    $(".jsOnly").show();

    var tmp;

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

    initPlaceHolders(document);
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

