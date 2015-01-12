
/* Taken and adapted from: */

/***********************************************
* Cool DHTML tooltip script II- © Dynamic Drive DHTML code library (www.dynamicdrive.com)
* This notice MUST stay intact for legal use
* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
***********************************************/

var offsetfromcursorX=12 //Customize x offset of tooltip
var offsetfromcursorY=10 //Customize y offset of tooltip

var offsetdivfrompointerX=10 //Customize x offset of tooltip DIV relative to pointer image
var offsetdivfrompointerY=14 //Customize y offset of tooltip DIV relative to pointer image. Tip: Set it to (height_of_pointer_image-1).

var ie=document.all
var ns6=document.getElementById && !document.all
var enabletip=false

var actobj=null;
var tipobj=null;
var pointerobj=null;

function ietruebody(){
	return (document.compatMode && document.compatMode!="BackCompat")? document.documentElement : document.body
}

function positiontip(e){
	if (enabletip){
		var curX=(ns6)?e.pageX : event.clientX+ietruebody().scrollLeft;
		var curY=(ns6)?e.pageY : event.clientY+ietruebody().scrollTop;
		//Find out how close the mouse is to the corner of the window
		var winwidth=ie&&!window.opera? ietruebody().clientWidth : window.innerWidth-20
		var winheight=ie&&!window.opera? ietruebody().clientHeight : window.innerHeight-20

		var rightedge=ie&&!window.opera? winwidth-event.clientX-offsetfromcursorX : winwidth-e.clientX-offsetfromcursorX
		var bottomedge=ie&&!window.opera? winheight-event.clientY-offsetfromcursorY : winheight-e.clientY-offsetfromcursorY

		var leftedge=(offsetfromcursorX<0)? offsetfromcursorX*(-1) : -1000

		//if the horizontal distance isn't enough to accomodate the width of the context menu
		if (rightedge<tipobj.offsetWidth){
			//move the horizontal position of the menu to the left by it's width
			tipobj.css('left', curX-tipobj.offsetWidth+"px")
		}
		else if (curX<leftedge)
		tipobj.css('left', "5px")
		else{
			//position the horizontal position of the menu where the mouse is positioned
			tipobj.css('left', curX+offsetfromcursorX-offsetdivfrompointerX+"px")
			pointerobj.css('left', curX+offsetfromcursorX+"px")
		}

		//same concept with the vertical position
		if (bottomedge<tipobj.offsetHeight){
			tipobj.css('top', curY-tipobj.offsetHeight-offsetfromcursorY+"px")
		}
		else{
			tipobj.css('top', curY+offsetfromcursorY+offsetdivfrompointerY+"px")
			pointerobj.css('top', curY+offsetfromcursorY+"px")
		}
		tipobj.css('visibility', "visible")
		pointerobj.css('visibility', "visible")
		pointerobj.css('visibility', "visible")
	}
}

function photoOff(){
	actobj.onmouseout = null;
	$('#doctor_image').src = blank_url;
	enabletip = false;
	tipobj.css('visibility', "hidden")
	pointerobj.css('visibility', "hidden")
	$('#doctor_name').innerHTML = "";
}

function photoOn(obj, image_url, text, service, phone) {
	actobj = obj;
	actobj.onmouseout = photoOff;
	pointerobj = $('#doctor_image');
	pointerobj.onerror = function() { pointerobj.onerror = null; pointerobj.src = error_url; };
	if (image_url != '') {
		pointerobj.attr('src', image_url);
	} else {
		pointerobj.attr('src', error_url);
	}
	tipobj = $('#doctor_photo_flyover');
	$('#doctor_name').html(text);
	$('#doctor_service').html(service);
	$('#doctor_phone').html(phone);
	//$('#doctor_photo_flyover').style.visibility = 'visible';
	document.onmousemove=positiontip;
	enabletip = true;
}

/* The following is for the Plastic Surgery flyover boxes.
   It doesn't really have anything to do with doctors,
   but since the css lables it "right_col_ul_doctors",
   why not put it that way in the javascript, too?
*/

var waiting = false;
var u;

function blockDisplay(e) {
	waiting = false;
	if (!e) var e = window.event;
	var tg = (window.event) ? e.srcElement : e.target;
	if (u != null && tg.id == 'plast_block_flyover') {
		u.style.display = 'none';
	}
	var v = tg.parentNode.getElementsByTagName('ul')[0];
	if (v == null) {
		v = tg.parentNode.parentNode.getElementsByTagName('ul')[0];
	}
	if (v != null) {
		u = v;
		u.style.display = 'block';
	}
}

function blockHide(e) {
	if (!e) var e = window.event;
	var tg = (window.event) ? e.srcElement : e.target;
	var v = tg.parentNode.getElementsByTagName('ul')[0];
	if (v != null) {
		u = v;
		waiting = true;
		setTimeout( function() {
			if (waiting) {
				u.style.display = 'none';
			}
		}, 200);
	}
}

function blockClear() {
	u.style.display = 'none';
}
