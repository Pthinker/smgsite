
$(document).ready(function() {
	launch_editor($("#id_description"), "SMG");
	launch_editor($("#id_notes"), "SMG");
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", true);
	});
	$("#id_title").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_title").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-");
		if (val.length > 40) {
			val.replace("(.*)_.*", "$1")
		}
		if(!e.attr("_changed") && val) {
			e.val(val);
		}
	});
	$("#id_title").css("width", "400px");
	$("#id_urlname").css("width", "400px");

});
