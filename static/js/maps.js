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
        //console.log('load map');
		var mapOptions = {
          zoom: 10,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(mapEl.get(0), mapOptions);
        var infowindows = [];
        var markersArray = [];
        var bounds = new google.maps.LatLngBounds();

        for (var i = 0; i < smg_locations.length; i++) {
        	var loc = smg_locations[i];
        	if (!loc.lat || !loc.lng)
        		continue;
	        var latlng = new google.maps.LatLng(loc.lat, loc.lng);
	        var url = loc.url || "javascript:void(0)";
	        
            var content = "<div class='scrollFix'><div>";
            content += "<p><a href='" + url + "'>" + loc.address + "</a></p></div></div>";

	        var infowindow = new google.maps.InfoWindow({
	            content: content
	        });
	        infowindows.push(infowindow);
	        var marker = new google.maps.Marker({
	            position: latlng,
	            map: map,
                icon: loc.marker,
	            title: loc.name || ("Location " + (i + 1)),
                zIndex: i
	        });
            markersArray.push(marker);
	        (function(infowindow, marker) {
	            google.maps.event.addListener(marker, 'mouseover', function() {
	                //for (var j = 0; j < infowindows.length; j++) {
	                //    infowindows[j].close();
	                //}
	                //infowindow.open(map, marker);
                    highestZIndex = 0;
                    for (var i = 0; i < markersArray.length; i++ ) {
                        // reset all markers
                        markersArray[i].setIcon(loc.marker);
                        //get highest zindex
                        tempZIndex = markersArray[i].getZIndex(); 
                        if (tempZIndex>highestZIndex) {  
                            highestZIndex = tempZIndex;  
                        } 
                    }
                    //marker.setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
                    marker.setZIndex(highestZIndex + 1);
                    marker.setIcon('http://1.bp.blogspot.com/_GZzKwf6g1o8/S6xwK6CSghI/AAAAAAAAA98/_iA3r4Ehclk/s1600/marker-green.png')
                    console.log(infowindow.getContent(map, marker));
                    $('#map-info').html(infowindow.getContent(map, marker));
	            });
	        })(infowindow, marker);
	        bounds.extend(latlng);
        }

        map.fitBounds(bounds);

	}

	// Handle directions for single location

	var directionsService = new google.maps.DirectionsService();

	window.smg_directions = function() {
		$("#route").html("");

		var directionsDisplay = new google.maps.DirectionsRenderer();
		directionsDisplay.setMap(map);
		directionsDisplay.setPanel($("#route").get(0));

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