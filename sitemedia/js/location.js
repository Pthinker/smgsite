var map;

function load() {
  if (GBrowserIsCompatible()) {
    map = new GMap2(document.getElementById("map"));
    map.setCenter(new GLatLng(glatitude, glongitude), 13);
	var point = new GLatLng(glatitude, glongitude);
	map.addOverlay(new GMarker(point, {clickable:false, title:"Our Office"}));
  }
}

//window.onload = load;
//window.onunload = GUnload;

var directionsPanel;
var directions;

function smg_directions() {
	$('#directions').html('');
	var address = $('#address_input').val();
	map = new GMap2($('#map')[0]);
    map.setCenter(new GLatLng(glatitude, glongitude), 13);
	directionsPanel = $('#directions')[0];
	directions = new GDirections(map, directionsPanel);
	var path = "from: " + address + " to: " + glatitude + "," + glongitude
	directions.load(path);
	$('html,body').scrollTop($('#location_map_directions_box').offset().top - 50);
}

function reset_input() {
	var el = $('#address_input');
	if (el.val() == 'Type starting address...') {
		el.val('');
	}
}
