function setFields() {
	var e1 = $("#id_email");
	var e2 = $("#id_urlname");
	var fn = $("#id_first_name").val()[0]
	var ln = $("#id_last_name").val()
	if(!e1.attr("_changed") && fn && ln) {
		e1.val(fn.toLowerCase() + ln.toLowerCase() + '@smgnj.com');
	}
	if(!e2.attr("_changed") && fn && ln) {
		e2.val(fn.toLowerCase() + ln.toLowerCase());
	}
	
}

$(document).ready(function() {
	launch_editor($("#id_touch.vLargeTextField"), "SMG");
	for (var i=0; i<10; i++) {
		var e = $("#id_accreditation_set-" + i + "-description");
		if (e) {
			e.css("width", "50em");
		}
	}
	var e = $("#id_accreditation_set-__prefix__-description");
	if (e) {
		e.css("width", "50em");
	}
	for (var i=0; i<10; i++) {
		var e = $("#id_degree_set-" + i + "-description");
		if (e) {
			e.css("width", "50em");
		}
	}
	var e = $("#id_degree_set-__prefix__-description");
	if (e) {
		e.css("width", "50em");
	}
	$("#id_email").change(function() {
		$("#id_email").attr("_changed", "true");
	});
	$("#id_urlname").change(function() {
		$("#id_urlname").attr("_changed", "true");
	});
	$("#id_first_name").keyup(setFields);
	$("#id_last_name").keyup(setFields);
});
