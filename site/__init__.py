from smgsite.settings import MEDIA_ROOT, MEDIA_URL

def unused_image_resize(model, field, IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT):
	get_height = 'get_%s_height' % field
	get_width = 'get_%s_width' % field
	image = getattr(model, field)
	height = getattr(model, get_height)()
	width = getattr(model, get_width)()
	if (IMAGE_MAX_HEIGHT and height > IMAGE_MAX_HEIGHT) or \
		(IMAGE_MAX_WIDTH and width > IMAGE_MAX_WIDTH):
		from PIL import Image, ImageOps
		import urllib
		import os
		from django.conf import settings
		image_name = image[0:image.rfind('.')]
		try:
			sized_image = Image.open(MEDIA_ROOT + image)
			sized_image.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT), Image.ANTIALIAS)
			sized_image = sized_image.convert("RGB")
			new_name = u'%s.jpg' % (image_name)
			sized_image.save(settings.MEDIA_ROOT + new_name, 'JPEG')
			if new_name != image:
				os.unlink(MEDIA_ROOT + image)
			setattr(model, field, new_name)
		except IOError:
			pass

def image_make_thumbnail(model, field, thumbnail, path, IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT):
	from PIL import Image, ImageOps
	import urllib
	import os
	from django.conf import settings
	get_height = 'get_%s_height' % field
	get_width = 'get_%s_width' % field
	image = getattr(model, field)
	image_name = image.name[0:image.name.rfind('.')]
	try:
		try:
			image.file.seek(0)
		except:
			pass
		unsized_image = Image.open(image.file)
		resized_image = unsized_image.copy()
		resized_image.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT), Image.ANTIALIAS)
		if resized_image.mode not in ('L', 'RGB'):
			resized_image = resized_image.convert('RGB')
		new_name = '%s__%s__.jpg' % (image_name, thumbnail)
                #print "Saving thumbnail to", MEDIA_ROOT + new_name
		resized_image.save(MEDIA_ROOT + '/' + new_name, 'JPEG')
		print model, thumbnail, MEDIA_URL + new_name
		setattr(model, thumbnail, MEDIA_URL + new_name)
	except IOError:
		pass

