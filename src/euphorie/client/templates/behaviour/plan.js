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
            $("#ActionPlanItemForm :input").each(function() {
                this.value = null;
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
        }
    },

    onAddMeasure: function(event) {
        event.preventDefault();
        var $new_tab = $("#measureTabs a:first").clone().insertBefore(this),
            $new_container = $("#ActionPlanItemForm .tab-container:first").clone().appendTo("#ActionPlanItemForm");

        $new_container.find(":input").each(function() {
            this.value = null;
        });
        $("#measureTabs a").removeClass("current");
        $new_tab.addClass("current");
        $("#ActionPlanItemForm .tab-container").removeClass("current").hide();
        $new_container.addClass("current").show();
        ActionPlan.UpdateNumbering();
    },

    findActive: function(measures) {
        var items = $.map(measures.find("dt"),
            function(a) { return $(a).hasClass("current"); });
        var active = $.inArray(true, items);

        return active;
    },

    UpdateNumbering: function() {
        var $tabs = $("#measureTabs > a"),
            $containers = $("#ActionPlanItemForm .tab-container"),
            i, $tab, $container, text;

        for (i=0; i<$tabs.length; i++) {
            $tab = $tabs.eq(i);
            $tab.attr("href", $tabs[i].hash.replace(/[0-9]+/, i+1));
            text = $tab[0].firstChild;
            text.textContent = text.textContent.replace(/[0-9]+/, i+1);
            $container = $containers.eq(i);
            $container
              .attr("id", $container.attr("id").replace(/[0-9]+/, i+1));
        }
    },


    MeasureHasData: function(m) {
        var data = $.map(m.find(":input:not(select)"),
                                   function(i) { return Boolean($(i).val()); });
        return $.inArray(true, data)!=-1;
    },

    toggleSolutionDropdown: function() {
        var $solutions = $("#standardSolutions"),
            position;
        
        if ($solutions.data("euphorie.visible")) {
            $solutions
                .data("euphorie.visible", false)
                .hide();
            $("html").unbind("click.fallback");
            return false;
        }

        $solutions.data("euphorie.visible", true);
        position=$(this).offset();
        $solutions
            .css({top: position.top, left: position.left})
            .show();
        $("html").bind("click.fallback", ActionPlan.toggleSolutionDropdown);
        return false;
    },

    addStandardSolution: function() {
        ActionPlan.toggleSolutionDropdown();
        alert("Whoop");

        var measures = $("#ActionPlanItemForm"),
            active = ActionPlan.findActive(measures);
            $measure = measures.find("dd").eq(active);

        if (ActionPlan.MeasureHasData($measure)) {
            if (!confirm(replace_confirm_text)) {
                return false;
            }
        }

        $measure.find(":input.actionPlan").val(
            $(this).find(".actionPlan").text());
        $measure.find(":input.preventionPlan").val(
            $(this).find(".preventionPlan").text());
        $measure.find(":input.requirements").val(
            $(this).find(".requirements").text());

        $("label.superImpose", $measure).each(setupSuperimpose);
    },
    
    init: function() {
        $(document)
            .on("click", "#measureTabs a", ActionPlan.onSwitchMeasure)
            .on("click", "#addMeasureButton", ActionPlan.onAddMeasure)
            .on("click", "#measureTabs .delete", ActionPlan.onDeleteMeasure)
            .on("click", ".button.solutions", ActionPlan.toggleSolutionDropdown)
            .on("click", "#standardSolutions li", ActionPlan.addStandardSolution);
    }
};

