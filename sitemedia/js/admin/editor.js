

toolbar_SMG = [
	['Source','-','Cut','Copy','Paste','PasteText','-','Undo','Redo','-','Find','Replace','-','SelectAll','SpellCheck','SpecialChar'],
	'/',
	['Bold','Italic','Underline','-','Subscript','Superscript','SpecialChar'],
	['NumberedList','BulletedList','-','JustifyCenter','Outdent','Indent','Blockquote','-','Styles','RemoveFormat'],
	'/',
	['Link','Unlink','Anchor','Image']
];


toolbar_Minimal = [
	['Source','Undo','Redo','-','Find','Replace','-','SelectAll','SpellCheck'],
	'/',
	['Bold','Italic','-','NumberedList','BulletedList','-','Link','Unlink','Image']
];


function launch_editor(element, toolset, width, height) {

	if (typeof width == "undefined") {
		width = 800;
	}
	if (typeof height == "undefined") {
		height = 500;
	}
	if (typeof toolset == "undefined") {
		toolset = toolbar_SMG;
	} else if (toolset == "SMG") {
		toolset = toolbar_SMG;
	} else if (toolset == "Minimal") {
		toolset = toolbar_Minimal;
	}
	element.ckeditor( function() { /* callback code */ }, {
		skin : 'office2003',
		toolbar : toolset,
		//uiColor : '#9AB8F3',
		width : width,
		height : height,
		stylesCombo_stylesSet : 'standard_styles:../js/admin/styles.js',
		filebrowserImageBrowseUrl : '/media/filemanager/browser/default/browser.html?Type=Image&Connector=/media/fckeditor/editor/filemanager/connectors/php/connector.php',
	});
        CKEDITOR.config.forcePasteAsPlainText = true ;
	
}
