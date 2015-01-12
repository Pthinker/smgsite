function logout() {
	dojo.xhrGet( {
		url: "/mysummitmedicalgroup/logout/?url=" + location.href, 
		handleAs: "json",
		timeout: 5000,
		load: function(response, ioArgs) {
			dijit.byId('mysmg_logout').show();
			return response;
		},
		error: function(response, ioArgs) {
			dijit.byId('mysmg_error').show();
			console.error("HTTP status code: ", ioArgs.xhr.status);
			return response;
		}
	});
}

function addPage() {
	if (typeof mysmg_title == "undefined") {
		var mysmg_title = document.title;
	}
	var url;
	if (typeof mysmg_model != "undefined") {
		url = "/mysummitmedicalgroup/add/?model=" + escape(mysmg_model) + "&pk=" + mysmg_pk;
	} else {
		url = "/mysummitmedicalgroup/add/?url=" + escape(location.href) + "&title=" + escape(mysmg_title);
	}
	document.location = url;
}