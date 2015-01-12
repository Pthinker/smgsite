
var counter = 0;

function toggleLocations(choice) {
	$('ul#main-location-' + choice).toggle();
	$('ul#main-location-' + choice + ' input:checked').each(function(i, e) {
		$(this).attr('checked', false);
	});
	loadDoctorResults();
}

function toggleChoices(choice) {
	$('#' + choice).toggle();
	if ($('#' + choice).is(':visible')) {
		$('#more-' + choice + ' span').html('-');
	} else {
		$('#more-' + choice + ' span').html('+');
	}
}

function loadDoctorResults(empty) {
	$('#loading-mask').width($('#doctor-finder-results').width());
	$('#loading-mask').height($('#doctor-finder-results').height());
	$('#loading-mask').css('z-index', 2);
	$('#loading-mask').show();
	$('.our_doctor').hide();
	$('.our_doctors').hide();

	// Notate on the form which choices have been made
	if (!empty) {
		var objs = new Array('location', 'specialty', 'gender', 'hospitals', 'languages');
		for (var x in objs) {
			var count = 0;
			var choices = "<ul>Current Selections:";
			$('#form-' + objs[x] + ' :checked').each(function(i, e) {
				count++;
				if (e.value.indexOf('(') == 0) {
					var value = e.value.substring(9).replace(' ', '_').replace("')", '');
					choices += "<li>" + $('#form-' + objs[x] + '-val-' + value).html() + "</li>";
				} else {
					choices += "<li>" + $('#form-' + objs[x] + '-val-' + e.value.replace(' ', '_')).html() + "</li>";
				}
			});
			choices += "</ul>";
			if (count > 0) {
				$('#form-' + objs[x] + '-selection').html(choices).show();
			} else {
				$('#form-' + objs[x] + '-selection').html("").hide();
			}
		}
	}

	if (empty) {
		data = '&ajax=True&counter=' + counter;
	} else {
		data = $('#finder-form').serialize() + '&ajax=True&counter=' + counter;
	}
	counter++;
	$.post('/doctor-finder/', data, function(data) {
		if (data.counter != counter - 1) { // Out of sync
			return;
		}
		var results = 0;
		$('#doctor-finder-results').fadeOut(200, function() {
			$.each(data.letters, function(index, letter) {
				var count = 0;
				var rowcount = 1;
				$.each(letter.list, function(index, row) {
					$.each(row, function(index, id) {
						results++;
						$('#div-row-' + letter.letter + '-' + rowcount).append($('#div-doctor-' + id));
						$('#div-doctor-' + id).show();
					});
					count++;
					if (count == 2) {
						count = 0;
						rowcount++;
					}
				});
				$('#div-letter-' + letter.letter).show();
			});
			$('input').removeAttr('disabled')
			$('#search-form span').css('color', '#000');
			$.each(data.form.location, function(index, value) {
				if (value.disabled == 'True') {
					key = value.key.replace(/'\)?/g, '');
					if (key.indexOf(("(None, ")) == 0) {
						key = key.substr(8);
						$('input[name="location"][value="' + value.key + '"]').attr('disabled', 'disabled');
						$('#form-location-val-' + key).css('color', '#888');
					} else {
						$('input[name="location"][value="' + value.key + '"]').attr('disabled', 'disabled');
						$('#form-location-val-' + key).css('color', '#888');
					}
				}
			});
			$.each(data.form.specialty, function(index, value) {
				if (value.disabled == 'True') {
					key = value.key;
					$('input[name="specialty"][value="' + key + '"]').attr('disabled', 'disabled');
					$('#form-specialty-val-' + key).css('color', '#888');
				}
			});
			$.each(data.form.gender, function(index, value) {
				if (value.disabled == 'True') {
					key = value.key;
					$('input[name="gender"][value="' + key + '"]').attr('disabled', 'disabled');
					$('#form-gender-val-' + key).css('color', '#888');
				}
			});
			$.each(data.form.hospitals, function(index, value) {
				if (value.disabled == 'True') {
					key = value.key;
					$('input[name="hospitals"][value="' + key + '"]').attr('disabled', 'disabled');
					$('#form-hospitals-val-' + key).css('color', '#888');
				}
			});
			$.each(data.form.languages, function(index, value) {
				if (value.disabled == 'True') {
					key = value.key;
					$('input[name="languages"][value="' + key + '"]').attr('disabled', 'disabled');
					$('#form-languages-val-' + key).css('color', '#888');
				}
			});
			/*if (results == 0) {
				$('.h1_sub_info').html("<p>No results were found for your search.</p>");
			} else {
				$('.h1_sub_info').html("<p>Search results displayed below:</p>");
			}*/
			if ($('#doctor-finder-results').height() > $('#loading-mask').height()) {
				$('#loading-mask').height($('#doctor-finder-results').height());
			}
			$('#doctor-finder-results').fadeIn(300, function() {
				$('#loading-mask').css('z-index', 0);
				$('#loading-mask').hide();
				$('html, body').animate({ scrollTop: 0 }, 'slow');
			});
		});
	}, 'json');

}

$(document).ready(function() {
	$('#search-form dl.main dd.form-list').hide();
	$('#search-form dl.more').hide();
	/*$('#finder-form').attr('action', function() {
		window.scroll(0,0);
		javascript:loadDoctorResults();
	});*/
	$('input.reset-form').click(function() {
		var objs = new Array('location', 'specialty', 'gender', 'hospitals', 'languages');
		for (var x in objs) {
			$('#form-' + objs[x] + '-selection').html("").hide();
			$('#form-' + objs[x]).hide();
		}
		$('#search-form dl.main dd ul ul').hide();
		$('span.expand').html('+');
		$('#finder-form').get(0).reset();
		/*@cc_on
		  loadDoctorResults(true);
		  @*/
	});
	$(':input:not([title="main"])').attr('onClick', 'javascript:loadDoctorResults();');
	$('#finder-form').submit(function() {
		loadDoctorResults();
		return false;
	});
	//$('input[name="Search"]').hide();
	$('dd.form-list ul li').append('<div class="clear"></div>');
	//$("dd ul li label").append('<div class="clear"></div>');
});

