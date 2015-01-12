
var prefix = ''
var request_id = 0;
var uri = '';
var sentSearch = new Array();
var static_img;
var busy_img;
var model = 'ALL';
var pulse = 0;

var sections = {"doctors\\.Doctor": 1, "services\\.Service": 1, "doctors\\.Specialty": 1};

function displayResults(data) {
	var response_id = data.getElementsByTagName( 'request_id' )[0].firstChild.nodeValue;
	if (response_id != request_id) {
		return;
	}
	/*$(prefix + '-image').src = static_img;*/
	pulse = false;
	var query = data.getElementsByTagName( 'query' )[0].firstChild.nodeValue;
	var expr = '((^|\\s)' + query + ')';
	var regex = new RegExp(expr, 'ig');
	var updated = new Object;
	var count = data.getElementsByTagName( 'count' )[0].firstChild.nodeValue;
	var other_data = '';
	if (count > 0) {
		// Set up the display areas
		$(prefix + '-block-Empty').hide();
		var groups = data.getElementsByTagName( 'result_group' );
		for (var i=0; i<groups.length; i++) {
			var group = groups[i];
			var group_name = group.getAttribute('name').replace('.', '\\.');
			var name = 'Other';
			var block = $(prefix + '-block-' + 'Other');
			var element = $(prefix + '-results-' + 'Other');
			if (sections[group_name]) {
				name = group_name;
				block = $(prefix + '-block-' + group_name);
				element = $(prefix + '-results-' + group_name);
			}
			var data = '<ul>';
			if (name == 'Other' && other_data.length > 0) {
				data = other_data;
			}
			var results = group.getElementsByTagName( 'result' );
			for (var j=0; j<results.length; j++) {
				var result = results[j];
				var text = result.getElementsByTagName( 'name' )[0].firstChild.nodeValue;
				var url = result.getElementsByTagName( 'url' )[0].firstChild.nodeValue;
				//text = text.replace(regex, "<strong>$1</strong>");
				if (name == 'doctors.Doctor') {	
					data = data + '<li>' + text + '</li>';
				/*} else if (name == 'Keywords' || name == 'services.Service') {
					data = data + '<li><a href="' + url + '"><span class="bold">' + text + '</span></a></li>';*/
				} else {
					data = data + '<li><a href="' + url + '">' + text + '</a></li>';
				}
			}
			if (name == 'relayhealth.Article') {
				data = data + '<li class="see_all"><a href="/library/">See all Live Well Library results</a></li>';
			}
			if (name == 'Other') {
				other_data = data;
			}
			data = data + '</ul>';
			element.html(data);
                        block.show();
                        element.show();
			updated[name] = 1;
		}
		for (var section in sections) {
			if (!updated[section]) {
				$(prefix + '-block-' + section).hide();
				$(prefix + '-results-' + section).hide();
				$(prefix + '-results-' + section).html('');
			}
		}
	} else {
		for (var section in sections) {
			$(prefix + '-block-' + section).hide();
			$(prefix + '-results-' + section).hide();
			$(prefix + '-results-' + section).html('');
		}
		$(prefix + '-block-Empty').html("<ul><li>No top matches found...</li></ul>");
		$(prefix + '-block-Empty').show();
	}
}

function unsearch(prefix, clear) {
	if (clear) {
		$(prefix + '-input').val('');
	}
	for (var section in sections) {
		if ($(prefix + '-block-' + section)) {
			$(prefix + '-block-' + section).hide();
			$(prefix + '-results-' + section).hide();
			$(prefix + '-results-' + section).html('');
		}
	}
	$(prefix + '-results').hide();
}

function pulseSearch() {
	if (pulse != 0) {
		if (pulse == 1) {
			$(prefix + '-block-Empty').innerHTML = "<ul><li>Searching</li></ul>";
		} else if (pulse == 2) {
			$(prefix + '-block-Empty').innerHTML = "<ul><li>Searching .</li></ul>";
		} else if (pulse == 3) {
			$(prefix + '-block-Empty').innerHTML = "<ul><li>Searching . .</li></ul>";
		} else if (pulse == 4) {
			$(prefix + '-block-Empty').innerHTML = "<ul><li>Searching . . .</li></ul>";
		}
		pulse++;
		if (pulse == 5) {
			pulse = 1;
		}
		setTimeout(pulseSearch, 500);
	}
}

function startSearch() {
	if (!sentSearch[request_id-1]) {
/*		$(prefix + '-image').src = busy_img; */
		pulse = 1;
		setTimeout(pulseSearch, 500);
		sentSearch[request_id-1] = true;
		var url = '/search/ajax/prefix/' + model + '/alpha/?request_id=' + request_id + '&name=' + uri;
                $.ajax({url: url, success: displayResults});
	}
}

function searchSite(name) {
	var element = $('#' + name);
	prefix = '#search';
	model = 'ALL';
	element.focusout(function() { setTimeout("unsearch('#search', true)", 400); });
	if (element.val().length >= 2) {
		if ($(prefix + '-results').not(":visible")) {
			$(prefix + '-block-Empty').show();
			$(prefix + '-block-Empty').html("<ul><li>Searching . . .</li></ul>");
			$(prefix + '-results').show();
		}
		var timeout = 400;
		if (request_id == 0) {
			timeout = 0;
		}
		sentSearch[request_id] = false;
		setTimeout(startSearch, 100);
		uri = encodeURIComponent(element.val());
		$(prefix + '-more-results-href').attr('href', '/search/?search-input=' + encodeURIComponent(element.val()));
		$(prefix + '-more-results-href2').attr('href', '/search/?search-input=' + encodeURIComponent(element.val()));
/*		$(prefix + '-more-results-href-img').href = '/search/?search-input=' + encodeURIComponent(element.value);*/
		request_id++;
	} else {
		unsearch(prefix, false);
	}
}

function searchDoctors(name) {
	var element = $(name);
	prefix = '#doctors';
	model = 'doctors.Doctor';
	element.observe('blur', function() { setTimeout("unsearch('doctors', true)", 400); });
	if (element.value.length >= 2) {
		if ($(prefix + '-results').style.display == 'none') {
			$(prefix + '-block-Empty').style.display = 'block';
			$(prefix + '-block-Empty').style.visibility = 'visible';		
			$(prefix + '-block-Empty').innerHTML = "<ul><li>Searching...</li></ul>";
			$(prefix + '-results').style.display = 'block';
		}
		var timeout = 400;
		if (request_id == 0) {
			timeout = 0;
		}
		sentSearch[request_id] = false;
		setTimeout(startSearch, 100);
		uri = encodeURIComponent(element.value);
		$(prefix + '-more-results-href').href = '/doctors/';
		$(prefix + '-more-results-href-img').href = '/doctors/';
		request_id++;
	} else {
		unsearch(prefix, false);
	}
}
