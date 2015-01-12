/*
Adapted from the CKeditor video code, as permitted by the GPL.

Original Code:
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.plugins.add( 'video',
{
	requires: ['dialog'],
	init : function( editor )
	{
		// Add the video and unvideo buttons.
		editor.addCommand( 'video', new CKEDITOR.dialogCommand( 'video' ) );
		editor.ui.addButton( 'Video',
			{
				label : 'Video',
				command : 'video',
			} );
		CKEDITOR.dialog.add( 'video', this.path + 'dialogs/video.js' );

	},

} );

