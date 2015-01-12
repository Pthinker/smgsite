// General JS site wide functions

var desktop = 768;
var mobile = 480;
var mode = get_mode();

function scroll_to_id(id){
    var tag = $("#"+ id);
    $('html,body').animate({scrollTop: tag.offset().top},'slow');
}


$('.service_list_select').change(function() {
   var service_path = $(this).val();
   if (service_path) {
        var path = '/service/'+service_path+'/'; 
        //console.log('Redirecting to '+ path);
        window.location = path;
   } 
});

// generic change url dropdown
$('select[rel=change-url]').change(function() {
   var path = $(this).val();
   if (path) {
        window.location = path;
   } 
});

function setup_popovers() {

    //$('.doctor-result a').popover({'trigger':'hover', 'placement': 'auto top'});

    // dont hide popover when mouse on it..
    $(".service-group a").popover({ trigger: "manual" , html: true, placement: 'auto right'})
    .on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 100);
    });
}




function setup_alpha_list(alpha, list) {
    if($(alpha).length) {

        var surname_chars = [];
        $(list).each(function() { 
            if (typeof $(this).data("char") != 'undefined') {
                surname_chars.push($(this).data("char"));
            }
        });

        $(alpha+" li").each(function() {
            if ($.inArray( $(this).data("char"), surname_chars ) >= 0) {
                $(this).removeClass('disabled');
                $(this).children('a').on('click', function( event ) {
                    event.preventDefault();
                    scroll_to_id($(this).data("id"));
                });
            }
        });
    };  
}


// run on page load
$(function() {
    if (mode == 'desktop') {
        setup_popovers();
    }

    $('img[usemap]').rwdImageMaps();

    // menu for mobile

    var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE ");
    if (msie > 0) {
        $("#mobile-nav").hide();
    } else {

        $("#mobile-nav").mmenu({
            // options object
            classes: "mm-white"
            //,zposition: 'front'
            //,moveBackground: 'false'
        }, {
           // configuration object
           //,hardwareAcceleration: false
           pageNodetype: "section"
            });

        $('#nav-toggle').on('click', function() {
            if($('#mobile-nav').hasClass('mm-opened')) {
                $("#mobile-nav").trigger("close.mm");

            } else {
                $("#mobile-nav").trigger("open.mm");
            }

        });
    }

    // setup  alpha-lists
    setup_alpha_list('#alpha-list', '#doctor-list .doctor-result');

    setup_alpha_list('#alpha-list', '.anchor');


    setup_facets();
    //position_search()

    // detect event switching between mobile and desktop
    $( "body" ).on( "mode_changed", function( event ) {
        //console.log( event.mode  );
        setup_facets();
        //position_search();

    });

    var offset = 220;
    var duration = 500;
    $(window).scroll(function() {
        if ($(this).scrollTop() > offset) {
            $('.back-to-top').fadeIn(duration);
        } else {
            $('.back-to-top').fadeOut(duration);
        }
    });
    
    $('.back-to-top').click(function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, duration);
        return false;
    })
      
});

function get_mode() {
    if ($( window ).width() <= desktop) {
        return'mobile';
    } else {
        return 'desktop';
    }
}

function setup_facets() {
    // colapse facets in mobile mode
    //console.log('setup facets for '+ mode);
    if (mode == 'desktop') {
        $( '#facets .panel-collapse' ).addClass('in').removeAttr( "style" );
    } else {
        $( '#facets .panel-collapse' ).removeClass('in');
    }
}

$( window ).resize(function() {
    position_search();
    //console.log($( window ).width());
    if (get_mode() != mode) {
        mode = get_mode();
        $( "body" ).trigger({
          type:"mode_changed",
          mode:mode
        });
    }
});

function emailPopup() {
    var title = escape(document.title);
    var url = escape(location.href);
    var newwin = window.open('/email-page/?title=' + title + '&referrer=' + url,'name','height=680,width=600,toolbar=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no');
}

function position_search() {
    var pos = $('.nav-search').position();
    var h = $('.nav-search').outerHeight();
    $('#search-results').css({
      top: pos.top + h - 2 + 'px',
      left: pos.left + 'px'
      
    });
}

function sizeText(size) {
    if (size == 'sml') {
        jQuery('#content').css("font-size",'.8em');
        jQuery('#text_sml_img').attr('src', text_sml_on);
        jQuery('#text_med_img').attr('src', text_med_off);
        jQuery('#text_big_img').attr('src', text_big_off);
    } else if (size == 'med') {
        jQuery('#content').css("font-size",'1em');
        jQuery('#text_sml_img').attr('src', text_sml_off);
        jQuery('#text_med_img').attr('src', text_med_on);
        jQuery('#text_big_img').attr('src', text_big_off);
    } else if (size == 'big') {
        jQuery('#content').css("font-size",'1.2em');
        jQuery('#text_sml_img').attr('src', text_sml_off);
        jQuery('#text_med_img').attr('src', text_med_off);
        jQuery('#text_big_img').attr('src', text_big_on);
    }
}

