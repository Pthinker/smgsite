$(document).ready(function() {
	launch_editor($("#id_description.vLargeTextField"), "SMG", 600, 300);
	
	$("#id_short_description").width(400);
	
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", true);
	});
	$("#id_title").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_title").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-");
		if(!e.attr("_changed") && val) {
			e.val(val);
		}
	});
});
