
$(document).ready(function() {
	launch_editor($("#id_content.vLargeTextField"));
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", true);
	});
	$("#id_headline").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_headline").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-");
		if (val.length > 40) {
			val.replace("(.*)_.*", "$1")
		}
		if(!e.attr("_changed") && val) {
			e.val(val);
		}
	});
	$("#id_headline").css("width", "400px");
	$("#id_urlname").css("width", "400px");

	if ($("#id_content_type option:selected").val() != 'N') {
		$('div.related_recipes').hide();
	}
	if (window.location.href.indexOf('?Nutrition') > 0) {
		$("#id_content_type").val("N");
		$("#id_content_type").attr("disabled", "disabled");
		$("#id_content_type").attr("name", "content-type-disp");
		$('#feature_form').append($('<input></input>').attr('name','content_type').attr('type','hidden').attr('value','N'));
	}
	else if (window.location.href.indexOf('?Fitness') > 0) {
		$("#id_content_type").val("F");
		$("#id_content_type").attr("disabled", "disabled");
		$("#id_content_type").attr("name", "content-type-disp");
		$('#feature_form').append($('<input></input>').attr('name','content_type').attr('type','hidden').attr('value','F'));
	}
	else {
		var val = $("#id_content_type").val();
		$("#id_content_type").attr("disabled", "disabled");
		$("#id_content_type").attr("name", "content-type-disp");
		$('#feature_form').append($('<input></input>').attr('name','content_type').attr('type','hidden').attr('value',val));
	}

});
