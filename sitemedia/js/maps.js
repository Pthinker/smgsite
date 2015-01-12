$(function() {

	var mapEl = $("#map");
	var map, latlng;

	if (window.glatitude && window.glongitude && mapEl.length) {

		// Single location

		latlng = new google.maps.LatLng(window.glatitude, window.glongitude);

		var mapOptions = {
          center: latlng,
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        mapEl.css({width: "100%", height: 400, marginLeft: 0});
        map = new google.maps.Map(mapEl.get(0), mapOptions);

        var content = $("#location_photo_address_box").text().replace(/Phone(.|[\r\n])+/, "").replace(/[\r\n\s]+$/, "").replace(/^[\r\n\s]+/, "").replace(/^(.+)/, "<b>$1</b>").replace(/[\r\n][\r\n\s]+/g, "<br>");
        var title = "Location Info";
        var infowindow = new google.maps.InfoWindow({
	    	content: content
		});
	    var marker = new google.maps.Marker({
	        position: latlng,
	        map: map,
	        title: title
	    });
	    map.setCenter(new google.maps.LatLng(latlng.lat() + 0.01, latlng.lng()));
	    infowindow.open(map, marker);

	} else if (window.smg_locations && mapEl.length) {

		// Multiple locations

		var mapOptions = {
          zoom: 10,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(mapEl.get(0), mapOptions);
        var infowindows = [];
        var bounds = new google.maps.LatLngBounds();

        for (var i = 0; i < smg_locations.length; i++) {
        	var loc = smg_locations[i];
        	if (!loc.lat || !loc.lng)
        		continue;
	        var latlng = new google.maps.LatLng(loc.lat, loc.lng);
	        var url = loc.url || "javascript:void(0)";
	        var content = "<a href='" + url + "'>" + (loc.image ? "<img src='" + loc.image + "' style='float:left;margin:0 10px 0 0;border:none'>" : "") + "</a><div style='float:right'><br>";
	        if (loc.name) {
	        	content += "<b><a href='" + url + "'>" + loc.name + "</a></b><br>" + (loc.address || "").replace(/\n/g, "<br>");
	        } else if (loc.address) {
	        	var addressLines = loc.address.split(/\n/);
	        	content += "<b><a href='" + url + "'>" + addressLines[0] + "</a></b><br>" + addressLines.slice(1).join("<br>");
	        }
	        content += "</div>";
	        var infowindow = new google.maps.InfoWindow({
	            content: content
	        });
	        infowindows.push(infowindow);
	        var marker = new google.maps.Marker({
	            position: latlng,
	            map: map,
	            title: loc.name || ("Location " + (i + 1))
	        });
	        (function(infowindow, marker) {
	            google.maps.event.addListener(marker, 'click', function() {
	                for (var j = 0; j < infowindows.length; j++) {
	                    infowindows[j].close();
	                }
	                infowindow.open(map, marker);
	            });
	        })(infowindow, marker);
	        bounds.extend(latlng);
        }

        map.fitBounds(bounds);

	}

	// Handle directions for single location

	var directionsService = new google.maps.DirectionsService();

	window.smg_directions = function() {
		$("#directions").html("");

		var directionsDisplay = new google.maps.DirectionsRenderer();
		directionsDisplay.setMap(map);
		directionsDisplay.setPanel($("#directions").get(0));

		var request = {
			origin: $("#address_input").val(),
			destination: latlng,
			travelMode: google.maps.TravelMode.DRIVING
		};
		directionsService.route(request, function(result, status) {
			if (status == google.maps.DirectionsStatus.OK) {
				directionsDisplay.setDirections(result);
			}
		});
	}

	window.reset_input = function() {
		var el = $('#address_input');
		if (el.val() == 'Type starting address...')
			el.val('');
	}

});