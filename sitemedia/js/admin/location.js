$(document).ready(function() {
	launch_editor($("#id_info"), "SMG");
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", true);
	});
	$("#id_name").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_name").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-").toLowerCase();
		if(!e.attr("_changed") && val) {
			e.val(val);
		}
	});
});
