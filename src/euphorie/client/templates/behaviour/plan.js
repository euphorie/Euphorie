(function ($) {
    $.fn.enableDatePicker = function () { 
        var lang = $("body").attr('lang');
        if (lang) {
            if (lang.indexOf('-') !== -1) {
                var parts = lang.split('-'),
                    language = parts[0],
                    territory= parts[1].toUpperCase();
                lang=language+"-"+territory;
                if ($.datepicker.regional[lang]===undefined) {
                    lang=language;
                }
            }
            if ($.datepicker.regional[lang]) {
                $.datepicker.setDefaults($.datepicker.regional[lang]);
            } else {
                // 'en' is not included in the obj, so fall back to en-GB. 
                // Otherwise we get a Taiwanese calendar.
                $.datepicker.setDefaults($.datepicker.regional['en-GB']);
            }
        }
        $(this).datepicker({
            showOn: "button",      
            dateFormat: "yy",
            onSelect: function (dateText, inst) {
                $(this).parent().find(".day").val(inst.selectedDay);
                $(this).parent().find(".month").val(inst.selectedMonth+1);
            }
        });
    };

    var ActionPlan = {
        onSwitchMeasure: function(event) {
            event.preventDefault();
            $("#measureTabs a").removeClass("current");
            $(this).addClass("current");
            $("#ActionPlanItemForm .tab-container").removeClass("current").hide();
            $(this.hash).addClass("current").show();
        },

        onDeleteMeasure: function(event) {
            event.preventDefault();
            event.stopPropagation();
            if (!confirm(delete_confirm_text)) {
                return false;
            }

            if ($("#measureTabs > a").length===1) {
                $("#ActionPlanItemForm :input:not(select)").each(function() {
                    $(this).removeAttr('value');
                });
                $("#ActionPlanItemForm select").each(function() {
                    $(this).children(':first').attr('selected', 'selected');
                });
            } else {
                var $tab = $(this).closest("a");
                $($tab[0].hash).remove();
                if ($tab.hasClass("current")) {
                    $("#measureTabs a:first").addClass("current");
                    $("#ActionPlanItemForm .tab-container:first").addClass("current").show();
                }
                $tab.remove();
                ActionPlan.UpdateNumbering();
            ActionPlan.chevronize();
            }
        },

        chevronize: function() {
            if ($("#measureTabs > a").length > 5) {
                $("#addMeasureButton").hide();
            } else {
                $("#addMeasureButton").show();
            }
        },

        prepClone: function(clone) {
            var number = $("#measureTabs > a").length;
            clone.find('#planning-start-day-1').attr('id', 'planning-start-day-' + number);
            clone.find('#planning-start-month-1').attr('id', 'planning-start-month-' + number);
            clone.find('#planning-start-year-1').attr('id', 'planning-start-year-' + number);

            clone.find('#planning-end-day-1').attr('id', 'planning-end-day-' + number);
            clone.find('#planning-end-month-1').attr('id', 'planning-end-month-' + number);
            clone.find('#planning-end-year-1').attr('id', 'planning-end-year-' + number);

            clone.find('.ui-datepicker-trigger').remove();
            clone.find('.enablePicker').each(function () {
                $(this).enableDatePicker();
            });
            return $(clone);
        },

        onAddMeasure: function(event) {
            event.preventDefault();
            var $new_tab = $("#measureTabs a:first").clone().insertBefore(this),
                $new_container = ActionPlan.prepClone($("#ActionPlanItemForm .tab-container:first").clone()).appendTo("#ActionPlanItemForm");

            $new_container.find(":input:not(select)").each(function() {
                $(this).removeAttr('value');
            });
            $new_container.find("select").each(function() {
                $(this).children(':first').attr('selected', 'selected');
            });
            $("#measureTabs a").removeClass("current");
            $new_tab.addClass("current");
            $("#ActionPlanItemForm .tab-container").removeClass("current").hide();
            $new_container.addClass("current").show('fast');
        initPlaceHolders($new_container);
        initTooltips($new_container);
            ActionPlan.UpdateNumbering();
            ActionPlan.chevronize();
        },

        findActive: function(measures) {
            var items = $.map(measures.find("dt"),
                function(a) { return $(a).hasClass("current"); });
            return $.inArray(true, items);
        },

        UpdateNumbering: function() {
            var $tabs = $("#measureTabs > a"),
                $containers = $("#ActionPlanItemForm .tab-container"),
                i, $tab, $container, text;

            for (i=0; i<$tabs.length; i++) {
                $tab = $tabs.eq(i);
                $tab.attr("href", $tabs[i].hash.replace(/[0-9]+/, i+1));
                text = $tab[0].firstChild;
                if (text.textContent){
                    text.textContent = text.textContent.replace(/[0-9]+/, i+1);
                } else {
                    text.data = text.data.replace(/[0-9]+/, i+1);
                }
                $container = $containers.eq(i);
                $container
                .attr("id", $container.attr("id").replace(/[0-9]+/, i+1));
            }
        },

        MeasureHasData: function(m) {
            var data = $.map(m.find(":input:not(select)"), 
                    function(i) { 
                        var val = $(i).val();
                        if (Boolean(val) && val !== $(i).attr('placeholder')) {
                            return true;
                        } else {
                            return false;
                        }
                    });
            return $.inArray(true, data)!==-1;
        },

        toggleSolutionDropdown: function() {
            var $solutions = $("#standardSolutions"),
                position;
            
            if ($solutions.data("euphorie.visible")) {
                $solutions
                    .data("euphorie.visible", false)
                    .hide();
                $("#standardSolutions li").off("click.euphorie");
                $("html").unbind("click.fallback");
                return false;
            }

            $solutions.data("euphorie.visible", true);
            position=$(this).offset();
            $solutions
                .css({top: position.top, left: position.left})
                .show();
            $("#standardSolutions li").on("click.euphorie", ActionPlan.addStandardSolution);
            $("html").bind("click.fallback", ActionPlan.toggleSolutionDropdown);
            return false;
        },

        addStandardSolution: function(event) {
            event.preventDefault();

            var $measure = $("#ActionPlanItemForm .tab-container.current");

            if (ActionPlan.MeasureHasData($measure)) {
                if (!confirm(replace_confirm_text)) {
                    return;
                }
            }
            $measure.find(":input.actionPlan").val(
                $(this).find(".actionPlan").text());
            $measure.find(":input.preventionPlan").val(
                $(this).find(".preventionPlan").text());
            $measure.find(":input.requirements").val(
                $(this).find(".requirements").text());
        },

        init: function() {
            $(document)
                .on("click", "#measureTabs a", ActionPlan.onSwitchMeasure)
                .on("click", "#addMeasureButton", ActionPlan.onAddMeasure)
                .on("click", "#measureTabs .delete", ActionPlan.onDeleteMeasure)
                .on("click", ".button.solutions", ActionPlan.toggleSolutionDropdown);

            $("#ActionPlanItemForm .tab-container:not(:first)").hide();
            $("#measureTabs a:first").addClass("current");
            $("#ActionPlanItemForm .tab-container:first").addClass('current');
            $('.enablePicker').each(function () {
                $(this).enableDatePicker();
            });
        }
    };
    $("#ActionPlanItemForm").ready(ActionPlan.init);
})(jQuery);

/*jslint plusplus: true, unparam: true, sloppy: true, white: true, browser: true, devel: true */
