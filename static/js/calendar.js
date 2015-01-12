$(document).ready(function() {
    var now = moment();
    var end = moment().add({months:24}) // 2 years
    $('#events-calendar').fullCalendar({
        editable: false,
        dragable: false,
        eventColor: '#ff9900',
        viewRender: function(view, ele) {
            if(view.intervalStart.month() == now.month() && view.intervalStart.year() == now.year()) { 
                $('.fc-button-prev').addClass("fc-state-disabled");
            } else { 
                $('.fc-button-prev').removeClass("fc-state-disabled"); 
            }

            if(view.intervalEnd.month() == end.month() && view.intervalEnd.year() == end.year()) { 
                $('.fc-button-next').addClass("fc-state-disabled"); 
            } else { 
                $('.fc-button-next').removeClass("fc-state-disabled"); 
            }
            // render monthly events
            
            if(view.intervalStart.month() == now.month()) {
                var event_date = now;
            } else {
                var event_date = view.intervalStart;
            }
            $( "#events-content" ).load( "/events/monthly/"+event_date.format('YYYY-MM-DD')+"/3/" );

        },
        events: {
            url: '/events/stream/'+now.format('YYYY-MM-DD')+'/'+end.format('YYYY-MM-DD')+'/',
            cache: true
        }
    });
    
});
