window.onload = function()
{
	launch_editor($("#id_blurb.vLargeTextField"), "SMG");
	$("#id_name").keyup(function() {
		var e = $("#id_urlname");
		var val = $("#id_name").val().replace(/ /g, "_").replace(/\W/g, "").replace(/_/g, "-");
		if(!e._changed && val) {
			e.val(val);
		}
	});
}
