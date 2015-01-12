var datepickers = datepickers || {}
    , eventDates = eventDates || {}
    MONTHS = {
        'January': 0,
        'February': 1,
        'March': 2,
        'April': 3,
        'May': 4,
        'June': 5,
        'July': 6,
        'August': 7,
        'September': 8,
        'October': 9,
        'November': 10,
        'December': 11
    };

function getInlineDatepickerMonthFor(order) {
    var validOrder = _.contains(['first', 'middle', 'last'], order),
        $dp = $('.datepicker .ui-datepicker-group-' + order + ' .ui-datepicker-title');
    var dpTitle = function() { return $dp.text().replace(/\u00A0/, ' ') };
    var month = Date.create(dpTitle());
    return validOrder ? month.getMonth() + 1 : null;
}

function sortEventsByMonth() {
    // Move all events into the unsorted list (which is hidden)
    $('.eventdate_choices label.box').appendTo('.eventdate_choices[data-month="unsorted"] .eventsinner');
    _.each(['first', 'middle', 'last'], function(order) {
        datepickers[order] = { month: getInlineDatepickerMonthFor(order) };
        $('.eventdate_choices[data-month="unsorted"] label.box[data-month="' + datepickers[order].month + '"]')
            .appendTo('.eventdate_choices .' + order + '_month');
    });
}

$(document).ready(function() {
    var eventDate, $choiceDateHiddenInputs, $choiceEl;

    $('.datepicker').datepicker({
        numberOfMonths: 3,
        onSelect: function (date, datepicker) {
            sortEventsByMonth()
        },
        onChangeMonthYear: function () {
            _.defer( function () { sortEventsByMonth() } );
        }
    });

    $('.eventdate_choices').on('change', 'input[name="eventdates"]', function(event) {
        var $evtTgt = $(event.target);
        $evtTgt.parents('label.box').toggleClass('eventdate_selected', $evtTgt.is(':checked'));
    });

    $choiceDateHiddenInputs = $('.eventdate_choices')
        .find('input[type="hidden"][name="eventdate_timelong"]');

    $choiceDateHiddenInputs.each(function() {
        $choiceEl = $(this).parents('label.box');
        var eventURL = $choiceEl.find('input[name="eventdate_absolute_url"]').val();
        var eventTitle = $(this).val().replace(/(.*?)\(.*?\)/, '$1');
        var parsedDate = $(this).val().replace(/.*\((.*?, [0-9:]+ [AP]M)(?: - [0-9:]+ [AP]M)?\)/, '$1');
        eventDate = Date.create(parsedDate);
        eventDates[$choiceEl.data('eventid')] = {
            title: eventTitle,
            startDate: eventDate
        };
        $choiceEl.attr({
            "data-month": eventDate.getMonth() + 1,
            "data-day": eventDate.getDate(),
            "data-year": eventDate.getFullYear()
        });
        $choiceEl
            .find('.date')
            .prepend(eventDate.format('{Mon}') + '<br>' + eventDate.format('{ord}'))
            .end()
            .find('.blockbox .title')
            .text(eventDate.format('{Dow}, {Mon} {ord}, {12hr}:{mm} {TT}'))
            .end()
            .find('.blockbox .subtitle')
            .html(
                eventTitle.length > 50
                    ? $('<p></p>').append($('<a/>', {"href": eventURL}).text(eventTitle.truncate(50)), $('<div/>').addClass('hoverbox').html($('<a/>', {"href": eventURL}).text(eventTitle))).html()
                    : $('<a/>', {"href": eventURL}).text(eventTitle)[0]
            );
    });

    sortEventsByMonth();

});

/*
*
* */
