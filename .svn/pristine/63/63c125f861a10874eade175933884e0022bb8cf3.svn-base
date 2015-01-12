import re
from datetime import datetime

from django.db import models
from django.core.cache import cache

import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.search.containers import SearchKey
from smgsite.site import image_make_thumbnail
from smgsite.settings import MEDIA_URL


#zip_re = re.compile(r'^\d{5}$')
#zip_validator = validators.MatchesRegularExpression(zip_re)
host_re = re.compile(r'^[\w-]+\.[\w-]+\.[\w-]+$')
site_re = re.compile(r'^[\w-]+\.[\w-]+\.[\w-]+.*$')

IMAGE_MAX_WIDTH = 140
IMAGE_MAX_HEIGHT = 196

THUMBNAIL_MAX_WIDTH = 100
THUMBNAIL_MAX_HEIGHT = 140

def isValidResource(field_data, all_data):
	print "Filed data is '%s'" % field_data
	if host_re.match(field_data):
		field_data = 'http://%s/' % field_data
	elif site_re.match(field_data):
		field_data = 'http://%s' % field_data
	if field_data.startswith('http://'):
		try:
			print 'Test URL'
			#validators.isExistingURL(field_data, field_data)
		except:
			print 'Raise exception'
			#raise validators.ValidationError('The URL %s is not active. Please make corrections.' % field_data)
	else:
		if not field_data[0] == '/':
			print 'Raise exception'
			#raise validators.ValidationError('The URL %s is a relative local link, which can have unintended results. Please make corrections so that the link begins with a /, as in /service/cardiology/.' % field_data)
	print "Searching", field_data
	try:
		existing = Resource.all_objects.get(url=field_data)
		print 'Raise exception'
		#raise validators.ValidationError('The URL %s is already registered as the resource %s. The same URL may not be registered multiple times.' % (field_data, existing))
	except Resource.DoesNotExist:
		pass


"""
class About(search.Model, models.Model):
	item_url = 'about'
	search_order = 4
	template_path = 'about'
	has_subpages = True
	search_placeholder = True
"""

class MissingImage(object):

    def __init__(self, name=None):
        self.name = name if name else 'no_image.jpg'

class Location(cms.Model, search.Model, models.Model):
	"""
	Model for SMG Locationes

	"""

	SHOW = 1
	HIDE = 0
	DISPLAY = (
		(u'1', 'Show in Lists'),
		(u'0', 'Hide from Lists'),
	)

	STATE_CHOICES = (
	    ('AL', 'Alabama'),
	    ('AK', 'Alaska'),
	    ('AS', 'American Samoa'),
	    ('AZ', 'Arizona'),
	    ('AR', 'Arkansas'),
	    ('CA', 'California'),
	    ('CO', 'Colorado'),
	    ('CT', 'Connecticut'),
	    ('DE', 'Delaware'),
	    ('DC', 'District of Columbia'),
	    ('FM', 'Federated States of Micronesia'),
	    ('FL', 'Florida'),
	    ('GA', 'Georgia'),
	    ('GU', 'Guam'),
	    ('HI', 'Hawaii'),
	    ('ID', 'Idaho'),
	    ('IL', 'Illinois'),
	    ('IN', 'Indiana'),
	    ('IA', 'Iowa'),
	    ('KS', 'Kansas'),
	    ('KY', 'Kentucky'),
	    ('LA', 'Louisiana'),
	    ('ME', 'Maine'),
	    ('MH', 'Marshall Islands'),
	    ('MD', 'Maryland'),
	    ('MA', 'Massachusetts'),
	    ('MI', 'Michigan'),
	    ('MN', 'Minnesota'),
	    ('MS', 'Mississippi'),
	    ('MO', 'Missouri'),
	    ('MT', 'Montana'),
	    ('NE', 'Nebraska'),
	    ('NV', 'Nevada'),
	    ('NH', 'New Hampshire'),
	    ('NJ', 'New Jersey'),
	    ('NM', 'New Mexico'),
	    ('NY', 'New York'),
	    ('NC', 'North Carolina'),
	    ('ND', 'North Dakota'),
	    ('MP', 'Northern Mariana Islands'),
	    ('OH', 'Ohio'),
	    ('OK', 'Oklahoma'),
	    ('OR', 'Oregon'),
	    ('PW', 'Palau'),
	    ('PA', 'Pennsylvania'),
	    ('PR', 'Puerto Rico'),
	    ('RI', 'Rhode Island'),
	    ('SC', 'South Carolina'),
	    ('SD', 'South Dakota'),
	    ('TN', 'Tennessee'),
	    ('TX', 'Texas'),
	    ('UT', 'Utah'),
	    ('VT', 'Vermont'),
	    ('VI', 'Virgin Islands'),
	    ('VA', 'Virginia'),
	    ('WA', 'Washington'),
	    ('WV', 'West Virginia'),
	    ('WI', 'Wisconsin'),
	    ('WY', 'Wyoming'),
	)

	DAY_CHOICES = (
		(u'1', 'Yes'),
		(u'0', 'No')
	)

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'location'
	search_order = 5
	search_limit = 10

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this location from display and search on the site.")
	display = models.CharField(max_length=1, default=u'1', choices=DISPLAY, help_text="Select Hide from Lists to prevent this location from displaying on the /location/ page.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for URL, e.g. enter 'berkeley_heights' to have this Doctor load at '/location/berkeley_heights/')")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	name = models.CharField(max_length=100, help_text="Enter the administrative name for this location, e.g. Summit Satellite.")
	display_name = models.CharField(max_length=100, blank=True, help_text="Enter the web display name for this location, e.g. Overlook Hopsital-MAC Building.")
	description = models.CharField(max_length=100, blank=True, help_text="(Optional) Enter a short desciption or other information, e.g. Behavioral Health Only.")
	address = models.CharField(max_length=100, help_text="Enter the street address for this location, e.g. 85 Woodland Road. Do not use this field for any information except a valid postal street address.")
	address2 = models.CharField(max_length=100, blank=True, help_text="(Optional) Continue the street address for this location, e.g. Suite 304).")
	city = models.CharField(max_length=100, help_text="Enter the city name for this location, e.g. Short Hills).")
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NJ')
	zipcode = models.CharField(max_length=5, help_text="Enter the zip code for this location.")
	phone = models.CharField(max_length=19, blank=True, help_text="Enter a phone number for this location.")
	fax = models.CharField(max_length=19, blank=True, help_text="Enter on optional fax number for this location.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/location-images', help_text="Upload an image for this location. This image will automatically be scaled to and %sx%s for display on the site." % (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
	image = models.ImageField(blank=True, null=True, editable=False, width_field='', height_field='', upload_to='db/location-images', )
	parking_code = models.CharField(max_length=5, blank=True, help_text="Enter an optional parking code for this location, e.g. B or ASC.")
	parking_name = models.CharField(max_length=50, blank=True, help_text="Enter an optional name for the parking area, e.g. Bensley Pavilion.")
	glatitude = models.CharField(max_length=25, blank=False, help_text="Enter latitude for google maps.")
	glongitude = models.CharField(max_length=25, blank=False, help_text="Enter longitude for google maps.")
	order = models.PositiveIntegerField(help_text="Enter a number for the order in which this location should be displayed in lists.")
	info = models.TextField(blank=True, help_text="Enter an optional description for this location.")
	starttime = models.TimeField(blank=True, null=True, help_text="Enter an optional 24-hour time for this location's standard opening time.")
	endtime = models.TimeField(blank=True, null=True, help_text="Enter an optional 24-hour time for this location's standard closing time.")
	monday = models.CharField(max_length=1, default=u'1', choices=DAY_CHOICES, help_text="Select if a standard weekday opening.")
	tuesday = models.CharField(max_length=1, default=u'1', choices=DAY_CHOICES, help_text="Select if a standard weekday opening.")
	wednesday = models.CharField(max_length=1, default=u'1', choices=DAY_CHOICES, help_text="Select if a standard weekday opening.")
	thursday = models.CharField(max_length=1, default=u'1', choices=DAY_CHOICES, help_text="Select if a standard weekday opening.")
	friday = models.CharField(max_length=1, default=u'1', choices=DAY_CHOICES, help_text="Select if a standard weekday opening.")
	hours_comments = models.TextField(blank=True, help_text="Enter optional comments for hours at this location.")

	class Meta:
		ordering = ['order', 'name']

	def __unicode__(self):
		if self.parking_name:
			return u'%s - %s' % (self.name, self.parking_name)
		else:
			return u'%s' % (self.name)

	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)

	def options(self):
		weekday = self.weekdayhours_set.all()
		saturday = self.saturdayhours_set.all()
		sunday = self.sundayhours_set.all()
		if weekday or saturday or sunday:
			return True
		return False

	def save(self, preview=True):
		# We use thumbnail in templates can preserve original image here I think.
		#if self.original_image:
			#image_make_thumbnail(self, 'original_image', 'image', 'db/location-images', IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT)
		super(Location, self).save(preview)
		cache.delete('finder-location-berkeley')
		cache.delete('finder-location-subberkeley')
		cache.delete('finder-location-notberkeley')
		snbkey = self.city.replace(' ', '_')
		cache.delete('finder-location-subnotberkeley-%s' % snbkey)
		cache.delete('finder-locations')

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = u'%s %s %s %s %s %s %s %s %s' % (self.name, self.address, self.address2, self.city, self.state, self.zipcode, self.phone, self.fax, self.parking_name)
		return SearchKey(self.pk, self.get_absolute_url(), self.order, self.name, self.name, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.order, self.name, self.keywords, self.keywords)

	@property
	def get_display_name(self):
		# noticed that sometimes there is no display name so will return the name instead
		if self.display_name:
			return self.display_name
		else:
			return self.name

	@property
	def display_address(self):
		# address format probably needs to be refactored
		address_list = filter(None, (self.display_name, self.address, self.address2, self.city, '%s %s' % (self.state, self.zipcode)))
		print ', '.join(address_list)
		return ', '.join(address_list)

	@property
	def display_image(self):
		if self.original_image:
			return self.original_image
		else:
			return MissingImage(name='db/image-library/location_default.jpg')


class WeekdayHours(cms.Model, models.Model):
	"""
	Model for additional weekday hours for locations
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove these hours from display on the site.")
	location = models.ForeignKey(Location)
	service = models.ForeignKey('services.Service', related_name='location_weekday_hours')
	position = models.PositiveSmallIntegerField(default=1, help_text="Enter a number to set the order for this location on display pages. Smaller numbers appear first.")
	hours = models.CharField(max_length=150, blank=True, help_text="Service hours eg 7:00 PM - 11:00 PM.")

	class Meta:
		verbose_name_plural = u'Weekday hours'

	def __unicode__(self):
		return u"%d: %s" % (self.pk, self.hours)

class SaturdayHours(cms.Model, models.Model):
	"""
	Model for additional Saturday hours for locations
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove these hours from display on the site.")
	location = models.ForeignKey(Location)
	service = models.ForeignKey('services.Service', related_name='location_saturday_hours')
	position = models.PositiveSmallIntegerField(default=1, help_text="Enter a number to set the order for this location on display pages. Smaller numbers appear first.")
	hours = models.CharField(max_length=150, blank=True, help_text="Service hours eg 7:00 PM - 11:00 PM.")

	class Meta:
		verbose_name_plural = u'Saturday hours'

	def __unicode__(self):
		return u"%d: %s" % (self.pk, self.hours)

class SundayHours(cms.Model, models.Model):
	"""
	Model for additional Sunday hours for locations
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove these hours from display on the site.")
	location = models.ForeignKey(Location)
	service = models.ForeignKey('services.Service', related_name='location_sunday_hours')
	position = models.PositiveSmallIntegerField(default=1, help_text="Enter a number to set the order for this location on display pages. Smaller numbers appear first.")
	hours = models.CharField(max_length=150, blank=True, help_text="Service hours eg 7:00 PM - 11:00 PM.")

	class Meta:
		verbose_name_plural = u'Sunday hours'

	def __unicode__(self):
		return u"%d: %s" % (self.pk, self.hours)

class Resource(cms.Model, models.Model):
	"""
	Model for on-site and off-site resource links.
		
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this article from display and search on the site.")
	name = models.CharField(max_length=50, unique=True, help_text="Enter a display name for this resource.")
	description = models.CharField(max_length=200, blank=True, help_text="Enter an optional description for this resource.")
	remote = models.BooleanField(editable=False, default=False, help_text="Check this box if the URL below is outsite the SMG site.")
	url = models.CharField(max_length=200, unique=True, help_text="Enter a URL for this resource (e.g. '/service/cardiology/' or 'http://www.webmd.com/').")
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return u'%s - %s' % (self.name, self.url)
	
	def save(self, preview=True):
		self.remote = False
		if host_re.match(self.url):
			self.url = 'http://%s/' % self.url
		elif site_re.match(self.url):
			self.url = 'http://%s' % self.url
		if self.url.startswith('http://'):
			self.remote = True
		super(Resource, self).save(preview)		


class MediaCategory(models.Model):
	"""
	Model for an media library categories.
		
	"""
	category = models.CharField(max_length=50, help_text="Enter a category name.")
	class Meta:
		verbose_name_plural = u'categories'
	def __unicode__(self):
		return '%s' % self.category


class Image(cms.Model, models.Model):
	"""
	Model for an image library.
		
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, editable=False)
	name = models.CharField(max_length=50, help_text="Enter a name for this image.")
	category = models.ForeignKey(MediaCategory, help_text="Select a category for this image.")
	description = models.CharField(max_length=200, blank=True, help_text="Enter an optional description for this image.")
	alt = models.CharField(max_length=75, help_text="Enter an alt tag value for this image. The text should state the function of the image, such as: 'Welcome to SMG' - 'Greetings from Our Staff' - 'Click to Submit'.")
	image = models.ImageField(width_field='', height_field='', upload_to='db/image-library', help_text="Image to upload to the image library.")
	thumbnail = models.ImageField(blank=True, width_field='', height_field='', upload_to='db/image-library', help_text="Optional thumbnail of image. Normally this is created from the image and scaled to be no larger than %sx%s" % (THUMBNAIL_MAX_WIDTH, THUMBNAIL_MAX_HEIGHT))
	
	def __unicode__(self):
		return u'%s' % (self.name)
	
	def get_absolute_url(self):
		return self.image.url
	
	def save(self, preview=True):
		if not self.thumbnail:
			image_make_thumbnail(self, 'image', 'thumbnail', 'db/image-library', THUMBNAIL_MAX_WIDTH, THUMBNAIL_MAX_HEIGHT)
		super(Image, self).save(preview)		


class MediaFile(cms.Model, models.Model):
	"""
	Model for a media library.
		
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, editable=False)
	category = models.ForeignKey(MediaCategory, help_text="Select a category for this file.")
	name = models.CharField(max_length=50, help_text="Enter a name for this file.")
	description = models.CharField(max_length=200, blank=True, help_text="Enter an optional description for this file.")
	mediafile = models.FileField(upload_to='db/media-library', help_text="File to upload to the media library.")
	
	def __unicode__(self):
		return u'%s' % (self.mediafile)
	
	def get_absolute_url(self):
		return self.get_mediafile_url()


def getKeywordChoices(model):
	print "Model is", model
	model = models.get_model(MODEL_APPS[model], model)
	return model.objects.all()


class HomepageImage(cms.Model, models.Model):
	"""
	Model for changing specific images on the homepage
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	PLACES = (
		('N', 'Our News'),
		('H', 'Health'),
		('E', 'Events'),
	)
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, editable=False)
	location = models.CharField(max_length=1, unique=True, choices=PLACES, help_text="Select the location for this homepage image.")
	image = models.ForeignKey(Image, help_text="Select the image to appear in the selecte location.")
	link = models.URLField(blank=True, help_text="Enter an optional link for this image.")

	class Meta:
		verbose_name = "Homepage Image"
		verbose_name_plural = "Homepage Images"

	def __unicode__(self):
		return u'Homepage image for %s' % (self.get_location_display())


class VideoTemplate(cms.Model, models.Model):
	"""
	Model for magnify.net video template code
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	# Each place can have a maximum number of videos
	# which are radomly rotated.
	PLACES = (
		('H', 'Homepage'),
	)
	LIMITS = (
		('H', 1),
	)
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, editable=False)
	location = models.CharField(max_length=1, choices=PLACES, help_text="Select the location for this video.")
	template = models.TextField(help_text="Paste the video template generated at magnify.net here.")
	description = models.CharField(verbose_name="Title", max_length=100, blank=True, help_text="Enter a title.")
	summary = models.TextField(blank=True, help_text="Enter a summary paragraph")

	class Meta:
		verbose_name = "Video Template"
		verbose_name_plural = "Video Templates"
	
	def location_count(self):
		count = [val for key,val in self.LIMITS if key==self.location][0]
		return count

	def __unicode__(self):
		return u'Video template for %s' % (self.get_location_display())

	def save(self, preview=True):
		from django import forms
		current = VideoTemplate.all_objects.filter(location=self.location)
		if len(current) >= self.location_count() and self not in current:
				raise forms.ValidationError('A limit of %d is set for templates for the location %s. Please remove one or more existing templates before attempting to add a new one.' % (self.location_count(), self.get_location_display()))
		super(VideoTemplate, self).save(preview=preview)


class UnsubscribeChoices(models.Model):
	reason = models.CharField(max_length=50)

	def __unicode__(self):
		return self.reason

class Unsubscribe(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	street_1 = models.CharField(max_length=100)
	street_2 = models.CharField(blank=True, max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2)
	zipcode = models.CharField(max_length=10)
	email = models.CharField(max_length=100, blank=True)
	reasons = models.ManyToManyField(UnsubscribeChoices)
	date_added = models.DateTimeField(auto_now_add=True)


class ImageSlideManager(models.Manager):
	def get_query_set(self):
		return super(ImageSlideManager, self).get_query_set().filter(
			active=u'1', 
			for_update__lte=1, 
			display_time__lte=datetime.now(),
			order__gt=0,
			)

class ImageSlide(cms.Model, models.Model):
	"""
		Model for homepage image slider
	"""

	qa_objects = cms.QAManager()
	objects = ImageSlideManager()
	all_objects = models.Manager()

	URL_TARGET = (
		('_self', 'Same Window'),
		('_blank', 'New Window'),
		)
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE)

	name = models.CharField(max_length=100, help_text="Enter a reference name for this slide.")
	display_time = models.DateTimeField(blank=True, default=datetime.now(), help_text='Choose a time when the image should be displayed from.')
	image = models.ImageField(upload_to='db/images/slider/', help_text="Image to use on the slider.")
	url = models.CharField(max_length=255,  help_text="URL for this slide, either relative or absolute.")
	target = models.CharField(max_length=10, choices=URL_TARGET, default="_self", help_text="Select the target location for the URL.")
	order = models.PositiveIntegerField(default=0, help_text="Rotation order.")

	class Meta:
		verbose_name = "Image Slide"
		verbose_name_plural = "Image Slides"
		ordering = ['order']

	def __unicode__(self):
		return self.name




