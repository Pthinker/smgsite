/*
Adapted from the CKeditor video code, as permitted by the GPL.

Original Code:
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.dialog.add( 'video', function( editor )
{
	var plugin = CKEDITOR.plugins.video;

	// Loads the parameters in a selected video to the video dialog fields.
	var javascriptProtocolRegex = /^javascript:/,
		emailRegex = /^mailto:([^?]+)(?:\?(.+))?$/,
		emailSubjectRegex = /subject=([^;?:@&=$,\/]*)/,
		emailBodyRegex = /body=([^;?:@&=$,\/]*)/,
		anchorRegex = /^#(.*)$/,
		urlRegex = /^((?:http|https|ftp|news):\/\/)?(.*)$/,
		selectableTargets = /^(_(?:self|top|parent|blank))$/,
		encodedEmailvideoRegex = /^javascript:void\(location\.href='mailto:'\+String\.fromCharCode\(([^)]+)\)(?:\+'(.*)')?\)$/,
		functionCallProtectedEmailvideoRegex = /^javascript:([^(]+)\(([^)]+)\)$/;

	var popupRegex =
		/\s*window.open\(\s*this\.href\s*,\s*(?:'([^']*)'|null)\s*,\s*'([^']*)'\s*\)\s*;\s*return\s*false;*\s*/;
	var popupFeaturesRegex = /(?:^|,)([^=]+)=(\d+|yes|no)/gi;

	var parsevideo = function( editor, element )
	{
		var href = ( element  && ( element.getAttribute( '_cke_saved_href' ) || element.getAttribute( 'href' ) ) ) || '',
		 	javascriptMatch,
			emailMatch,
			anchorMatch,
			urlMatch,
			retval = {};

		if ( ( javascriptMatch = href.match( javascriptProtocolRegex ) ) )
		{
			if ( emailProtection == 'encode' )
			{
				href = href.replace( encodedEmailvideoRegex,
						function ( match, protectedAddress, rest )
						{
							return 'mailto:' +
							       String.fromCharCode.apply( String, protectedAddress.split( ',' ) ) +
							       ( rest && unescapeSingleQuote( rest ) );
						});
			}
			// Protected email video as function call.
			else if ( emailProtection )
			{
				href.replace( functionCallProtectedEmailvideoRegex, function( match, funcName, funcArgs )
				{
					if ( funcName == compiledProtectionFunction.name )
					{
						retval.type = 'email';
						var email = retval.email = {};

						var paramRegex = /[^,\s]+/g,
							paramQuoteRegex = /(^')|('$)/g,
							paramsMatch = funcArgs.match( paramRegex ),
							paramsMatchLength = paramsMatch.length,
							paramName,
							paramVal;

						for ( var i = 0; i < paramsMatchLength; i++ )
						{
							paramVal = decodeURIComponent( unescapeSingleQuote( paramsMatch[ i ].replace( paramQuoteRegex, '' ) ) );
							paramName = compiledProtectionFunction.params[ i ].toLowerCase();
							email[ paramName ] = paramVal;
						}
						email.address = [ email.name, email.domain ].join( '@' );
					}
				} );
			}
		}

		if ( !retval.type )
		{
			retval.type = 'url';
		}

		// Load target and popup settings.
		if ( element )
		{
			var target = element.getAttribute( 'target' );
			retval.target = {};
			retval.adv = {};

			// IE BUG: target attribute is an empty string instead of null in IE if it's not set.
			if ( !target )
			{
				var onclick = element.getAttribute( '_cke_pa_onclick' ) || element.getAttribute( 'onclick' ),
					onclickMatch = onclick && onclick.match( popupRegex );
				if ( onclickMatch )
				{
					retval.target.type = 'popup';
					retval.target.name = onclickMatch[1];

					var featureMatch;
					while ( ( featureMatch = popupFeaturesRegex.exec( onclickMatch[2] ) ) )
					{
						if ( featureMatch[2] == 'yes' || featureMatch[2] == '1' )
							retval.target[ featureMatch[1] ] = true;
						else if ( isFinite( featureMatch[2] ) )
							retval.target[ featureMatch[1] ] = featureMatch[2];
					}
				}
			}
			else
			{
				var targetMatch = target.match( selectableTargets );
				if ( targetMatch )
					retval.target.type = retval.target.name = target;
				else
				{
					retval.target.type = 'frame';
					retval.target.name = target;
				}
			}

			var me = this;
			var advAttr = function( inputName, attrName )
			{
				var value = element.getAttribute( attrName );
				if ( value !== null )
					retval.adv[ inputName ] = value || '';
			};
			advAttr( 'advId', 'id' );
			advAttr( 'advLangDir', 'dir' );
			advAttr( 'advAccessKey', 'accessKey' );
			advAttr( 'advName', 'name' );
			advAttr( 'advLangCode', 'lang' );
			advAttr( 'advTabIndex', 'tabindex' );
			advAttr( 'advTitle', 'title' );
			advAttr( 'advContentType', 'type' );
			advAttr( 'advCSSClasses', 'class' );
			advAttr( 'advCharset', 'charset' );
			advAttr( 'advStyles', 'style' );
		}

		// Find out whether we have any anchors in the editor.
		// Get all IMG elements in CK document.
		var elements = editor.document.getElementsByTag( 'img' ),
			realAnchors = new CKEDITOR.dom.nodeList( editor.document.$.anchors ),
			anchors = retval.anchors = [];

		for ( var i = 0; i < elements.count() ; i++ )
		{
			var item = elements.getItem( i );
			if ( item.getAttribute( '_cke_realelement' ) && item.getAttribute( '_cke_real_element_type' ) == 'anchor' )
				anchors.push( editor.restoreRealElement( item ) );
		}

		for ( i = 0 ; i < realAnchors.count() ; i++ )
			anchors.push( realAnchors.getItem( i ) );

		for ( i = 0 ; i < anchors.length ; i++ )
		{
			item = anchors[ i ];
			anchors[ i ] = { name : item.getAttribute( 'name' ), id : item.getAttribute( 'id' ) };
		}

		// Record down the selected element in the dialog.
		this._.selectedElement = element;

		return retval;
	};

	var setupParams = function( page, data )
	{
		if ( data[page] )
			this.setValue( data[page][this.id] || '' );
	};

	var setupPopupParams = function( data )
	{
		return setupParams.call( this, 'target', data );
	};

	var setupAdvParams = function( data )
	{
		return setupParams.call( this, 'adv', data );
	};

	var commitParams = function( page, data )
	{
		if ( !data[page] )
			data[page] = {};

		data[page][this.id] = this.getValue() || '';
	};

	var commitPopupParams = function( data )
	{
		return commitParams.call( this, 'target', data );
	};

	var commitAdvParams = function( data )
	{
		return commitParams.call( this, 'adv', data );
	};

	function unescapeSingleQuote( str )
	{
		return str.replace( /\\'/g, '\'' );
	}

	function escapeSingleQuote( str )
	{
		return str.replace( /'/g, '\\$&' );
	}

	var emailProtection = editor.config.emailProtection || '';

	// Compile the protection function pattern.
	if ( emailProtection && emailProtection != 'encode' )
	{
		var compiledProtectionFunction = {};

		emailProtection.replace( /^([^(]+)\(([^)]+)\)$/, function( match, funcName, params )
		{
			compiledProtectionFunction.name = funcName;
			compiledProtectionFunction.params = [];
			params.replace( /[^,\s]+/g, function( param )
			{
				compiledProtectionFunction.params.push( param );
			} );
		} );
	}

	function protectEmailvideoAsFunction( email )
	{
		var retval,
			name = compiledProtectionFunction.name,
			params = compiledProtectionFunction.params,
			paramName,
			paramValue;

		retval = [ name, '(' ];
		for ( var i = 0; i < params.length; i++ )
		{
			paramName = params[ i ].toLowerCase();
			paramValue = email[ paramName ];

			i > 0 && retval.push( ',' );
			retval.push( '\'',
						 paramValue ?
						 escapeSingleQuote( encodeURIComponent( email[ paramName ] ) )
						 : '',
						 '\'');
		}
		retval.push( ')' );
		return retval.join( '' );
	}

	function protectEmailAddressAsEncodedString( address )
	{
		var charCode,
			length = address.length,
			encodedChars = [];
		for ( var i = 0; i < length; i++ )
		{
			charCode = address.charCodeAt( i );
			encodedChars.push( charCode );
		}
		return 'String.fromCharCode(' + encodedChars.join( ',' ) + ')';
	}

	var commonLang = editor.lang.common,
		videoLang = 'Video';

	return {
		title : 'Video',
		minWidth : 350,
		minHeight : 230,
		contents : [
			{
				id : 'info',
				label : 'This is the label',
				title : 'This is the title',
				elements :
				[
					{
						type : 'vbox',
						id : 'urlOptions',
						children :
						[
							{
								type : 'hbox',
								widths : [ '25%', '75%' ],
								children :
								[
									{
										id : 'protocol',
										type : 'select',
										label : commonLang.protocol,
										'default' : 'http://',
										items :
										[
											// Force 'ltr' for protocol names in BIDI. (#5433)
											[ 'http://\u200E', 'http://' ],
											[ 'https://\u200E', 'https://' ],
											[ 'ftp://\u200E', 'ftp://' ],
											[ 'news://\u200E', 'news://' ],
											[ '<other>' , '' ]
										],
										setup : function( data )
										{
											if ( data.url )
												this.setValue( data.url.protocol || '' );
										},
										commit : function( data )
										{
											if ( !data.url )
												data.url = {};

											data.url.protocol = this.getValue();
										}
									},
									{
										type : 'text',
										id : 'url',
										label : commonLang.url,
										required: true,
										onLoad : function ()
										{
											this.allowOnChange = true;
										},
										onKeyUp : function()
										{
											this.allowOnChange = false;
											var	protocolCmb = this.getDialog().getContentElement( 'info', 'protocol' ),
												url = this.getValue(),
												urlOnChangeProtocol = /^(http|https|ftp|news):\/\/(?=.)/gi,
												urlOnChangeTestOther = /^((javascript:)|[#\/\.\?])/gi;

											var protocol = urlOnChangeProtocol.exec( url );
											if ( protocol )
											{
												this.setValue( url.substr( protocol[ 0 ].length ) );
												protocolCmb.setValue( protocol[ 0 ].toLowerCase() );
											}
											else if ( urlOnChangeTestOther.test( url ) )
												protocolCmb.setValue( '' );

											this.allowOnChange = true;
										},
										onChange : function()
										{
											if ( this.allowOnChange )		// Dont't call on dialog load.
												this.onKeyUp();
										},
										validate : function()
										{
											var dialog = this.getDialog();

											if ( dialog.getContentElement( 'info', 'videoType' ) &&
													dialog.getValueOf( 'info', 'videoType' ) != 'url' )
												return true;

											if ( this.getDialog().fakeObj )	// Edit Anchor.
												return true;

											var func = CKEDITOR.dialog.validate.notEmpty( videoLang.noUrl );
											return func.apply( this );
										},
										setup : function( data )
										{
											this.allowOnChange = false;
											if ( data.url )
												this.setValue( data.url.url );
											this.allowOnChange = true;

										},
										commit : function( data )
										{
											// IE will not trigger the onChange event if the mouse has been used
											// to carry all the operations #4724
											this.onChange();

											if ( !data.url )
												data.url = {};

											data.url.url = this.getValue();
											this.allowOnChange = false;
										}
									}
								],
								setup : function( data )
								{
									if ( !this.getDialog().getContentElement( 'info', 'videoType' ) )
										this.getElement().show();
								}
							},
						]
					},
				]
			},
		],
		onShow : function()
		{
			this.fakeObj = false;

			var editor = this.getParentEditor(),
				selection = editor.getSelection(),
				element = null;

			// Fill in all the relevant fields if there's already one video selected.
			if ( ( element = plugin.getSelectedvideo( editor ) ) && element.hasAttribute( 'href' ) )
				selection.selectElement( element );
			else if ( ( element = selection.getSelectedElement() ) && element.is( 'img' )
					&& element.getAttribute( '_cke_real_element_type' )
					&& element.getAttribute( '_cke_real_element_type' ) == 'anchor' )
			{
				this.fakeObj = element;
				element = editor.restoreRealElement( this.fakeObj );
				selection.selectElement( this.fakeObj );
			}
			else
				element = null;

			this.setupContent( parsevideo.apply( this, [ editor, element ] ) );
		},
		onOk : function()
		{
			var attributes = { href : 'javascript:void(0)/*' + CKEDITOR.tools.getNextNumber() + '*/' },
				removeAttributes = [],
				data = { href : attributes.href },
				me = this,
				editor = this.getParentEditor();

			this.commitContent( data );

			// Compose the URL.
			switch ( data.type || 'url' )
			{
				case 'url':
					var protocol = ( data.url && data.url.protocol != undefined ) ? data.url.protocol : 'http://',
						url = ( data.url && data.url.url ) || '';
					attributes._cke_saved_href = ( url.indexOf( '/' ) === 0 ) ? url : protocol + url;
					break;
			}

			// Popups and target.
			if ( data.target )
			{
				if ( data.target.type == 'popup' )
				{
					var onclickList = [ 'window.open(this.href, \'',
							data.target.name || '', '\', \'' ];
					var featureList = [ 'resizable', 'status', 'location', 'toolbar', 'menubar', 'fullscreen',
							'scrollbars', 'dependent' ];
					var featureLength = featureList.length;
					var addFeature = function( featureName )
					{
						if ( data.target[ featureName ] )
							featureList.push( featureName + '=' + data.target[ featureName ] );
					};

					for ( var i = 0 ; i < featureLength ; i++ )
						featureList[i] = featureList[i] + ( data.target[ featureList[i] ] ? '=yes' : '=no' ) ;
					addFeature( 'width' );
					addFeature( 'left' );
					addFeature( 'height' );
					addFeature( 'top' );

					onclickList.push( featureList.join( ',' ), '\'); return false;' );
					attributes[ '_cke_pa_onclick' ] = onclickList.join( '' );

					// Add the "target" attribute. (#5074)
					removeAttributes.push( 'target' );
				}
				else
				{
					if ( data.target.type != 'notSet' && data.target.name )
						attributes.target = data.target.name;
					else
						removeAttributes.push( 'target' );

					removeAttributes.push( '_cke_pa_onclick', 'onclick' );
				}
			}

			// Advanced attributes.
			if ( data.adv )
			{
				var advAttr = function( inputName, attrName )
				{
					var value = data.adv[ inputName ];
					if ( value )
						attributes[attrName] = value;
					else
						removeAttributes.push( attrName );
				};

				if ( this._.selectedElement )
					advAttr( 'advId', 'id' );
				advAttr( 'advLangDir', 'dir' );
				advAttr( 'advAccessKey', 'accessKey' );
				advAttr( 'advName', 'name' );
				advAttr( 'advLangCode', 'lang' );
				advAttr( 'advTabIndex', 'tabindex' );
				advAttr( 'advTitle', 'title' );
				advAttr( 'advContentType', 'type' );
				advAttr( 'advCSSClasses', 'class' );
				advAttr( 'advCharset', 'charset' );
				advAttr( 'advStyles', 'style' );
			}

			var element = CKEDITOR.dom.element.createFromHtml( '<blap>' + attributes._cke_saved_href + '</strong>', editor.document );
			console.debug(element);
			editor.insertElement(element);
		},
		onLoad : function()
		{
		},
		// Inital focus on 'url' field if video is of type URL.
		onFocus : function()
		{
			var videoType = this.getContentElement( 'info', 'videoType' ),
					urlField;
			if ( videoType && videoType.getValue() == 'url' )
			{
				urlField = this.getContentElement( 'info', 'url' );
				urlField.select();
			}
		}
	};
});

