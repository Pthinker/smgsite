jQuery.noConflict();

var start = 0;
var interval;
var show_time = 10000;
var url = "http://www.summitmedicalgroup.com/article-leader/";

jQuery(document).ready(function(){			 
	var thumb_width = jQuery(".smg-slider-thumbs li").width();
		
	jQuery(".smg-slider-thumbs li").each(function(i){
		jQuery(this).css("left",i*thumb_width+"px");
	});
	
	jQuery(".smg-slider-thumbs li").click(function(){
		jQuery(".smg-slider-thumbs li").removeClass("active");
		jQuery(this).addClass("active");
		start = jQuery(this).index() - 1;
		call_next();
	});

	interval = setInterval(call_next,show_time);
	jQuery(".smg-slider-thumbs li:eq(0)").addClass("active");
		
	/*jQuery("#control-next").click(function(){
		clearInterval( interval );
		interval = setInterval(call_next,show_time);
		call_next();	
	});*/
});

function call_next()
{
	clearInterval( interval );
	interval = setInterval(call_next,show_time);
	
	start++;
	start = ( start >= jQuery(".smg-slider-thumbs li").length ) ? 0 : start;
	jQuery(".smg-slider > div:first-child").animate({opacity: 0}, 500,"",load_next);
	jQuery(".smg-slider-thumbs li").removeClass("active");
	jQuery(".smg-slider-thumbs li:eq("+start+")").addClass("active");
}
function load_next()
{
	jQuery.get(url+start,function(data){
		jQuery(".smg-slider > div:first-child").html("").append(data);
		jQuery(".smg-slider > div:first-child").animate({opacity: 1.0}, 500);
	});	
}
