var share_flyover;
var firstClick = new Array(100);

function firstRemove() {
	for (i=1; i<firstClick.length; i++)
		if (firstClick[i]==this) return;
	firstClick[firstClick.length]=this;
	this.value='';
 }

function shareFlyoverShow() { if (share_flyover) share_flyover.style.display='block'; }
function shareFlyoverHide() { if (share_flyover) share_flyover.style.display='none'; }

function defaultActions() {
	if (document.getElementById) {
		if (share_anchor=document.getElementById('share_flyover_link')) {
			share_anchor.onmouseover=shareFlyoverShow;
			share_anchor.onmouseout=shareFlyoverHide;
		}
		if (share_flyover=document.getElementById('share_flyover')) {
			share_flyover.onmouseover=shareFlyoverShow;
			share_flyover.onmouseout=shareFlyoverHide;
		}
	}
}

window.onload = defaultActions;

function highlight(element, norm, big) {
	element.onmouseout = function() { element.style.width = norm; element.style.marginLeft = "0px"; }
	element.style.width = big;
	element.style.marginLeft = "-1px";
}

function sizeText(size) {
	if (size == 'sml') {
		jQuery('#main_block').css("font-size",'.8em');
		jQuery('#text_sml_img').attr('src', text_sml_on);
		jQuery('#text_med_img').attr('src', text_med_off);
		jQuery('#text_big_img').attr('src', text_big_off);
	} else if (size == 'med') {
		jQuery('#main_block').css("font-size",'1em');
		jQuery('#text_sml_img').attr('src', text_sml_off);
		jQuery('#text_med_img').attr('src', text_med_on);
		jQuery('#text_big_img').attr('src', text_big_off);
	} else if (size == 'big') {
		jQuery('#main_block').css("font-size",'1.2em');
		jQuery('#text_sml_img').attr('src', text_sml_off);
		jQuery('#text_med_img').attr('src', text_med_off);
		jQuery('#text_big_img').attr('src', text_big_on);
	}
}

function printablePage() {
	var url = location.href;
        var baseurl = url + '?';
        if (url.indexOf('?') != -1) {
            baseurl = url + '&';
        }
	var newwin = window.open(baseurl + 'printable=true','name','height=600,width=960,toolbar=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no');
}

function emailPopup() {
	var title = escape(document.title);
	var url = escape(location.href);
	var newwin = window.open('/email-page/?title=' + title + '&referrer=' + url,'name','height=680,width=600,toolbar=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no');
}
