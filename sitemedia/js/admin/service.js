$(document).ready(function() {
	launch_editor($("#id_content"), "SMG");
	launch_editor($("#id_offerings"), "SMG");
	launch_editor($("#id_learn_more"), "SMG");
	launch_editor($("#id_patient_tools"), "SMG");
	launch_editor($("#id_location"), "SMG");
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", true);
	});
	$("#id_name").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_name").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-");
		if(!e.attr("_changed") && val) {
			e.val(val);
		}
	});
});
