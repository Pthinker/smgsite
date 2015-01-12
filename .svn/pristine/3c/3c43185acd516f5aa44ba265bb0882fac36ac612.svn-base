import re
from datetime import datetime, date
from django.db import models
from smgsite.settings import MEDIA_URL
import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.search.containers import SearchKey
from smgsite.site import image_make_thumbnail
from smgsite.doctors.models import Doctor
from smgsite.services.models import Service
from smgsite.site.models import Location

IMAGE_MAX_WIDTH = 240
IMAGE_MAX_HEIGHT = 240

ICON_MAX_WIDTH = 65
ICON_MAX_HEIGHT = 65

zero_re = re.compile(r' 0(\d)')
whitespace_re = re.compile(r'\S')
#zip_re = re.compile(r'^\d{5}$')
#zip_validator = validators.MatchesRegularExpression(zip_re)

class EventManager(cms.Manager):
	"""
	Manager for event listings
	
	Events are only listed and searchable on the site before and including the date of the event.
	After that, they are removed from the site indexes and search.
	"""
	def get_query_set(self):
		return super(EventManager, self).get_query_set().filter(eventtime__enddate__gte=datetime.now())

class ClassManager(cms.Manager):
	"""
	Manager for class listings
	
	Events are only listed and searchable on the site before and including the date of the event.
	After that, they are removed from the site indexes and search.
	"""
	def get_query_set(self):
		return super(ClassManager, self).get_query_set().filter(enddate__gte=datetime.now(), active='1')

class EventDisplayManager(cms.Manager):
	"""
	Manager for event display
	
	Events must be displayed on the site even after the date of the event has passed. This is
	because search engines may still list the site for some time.
	"""
	def get_query_set(self):
		return super(EventDisplayManager, self).get_query_set()


class Event(cms.Model, search.Model, models.Model, cms.ClonableMixin):
	"""
	Model for Events
	
	This is a model for the events entered and displayed on the website.
	"""
	
	qa_objects = cms.QAManager()
	objects = models.Manager()
	all_objects = models.Manager()
	display_objects = EventDisplayManager()
	item_url = 'event'
	search_order = 4
	search_limit = 10
	
	TYPES = (
		('P', 'Program'),
		('L', 'Lecture'),
		('E', 'Exhibit'),
		('S', 'Support Group'),
		('W', 'Workshop'),
		('F', 'Festival'),
	)

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this event from display and search on the site. Registration reminders will not be sent for an inactive event. However, a cancellation message must be provided manually with the Notfication field below.")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Diabetes-Lecture' to have this Event load at '/event/Diabetes-Lecture/'). This is normally created for you from the title.")
	#startdate = models.DateField(help_text="Enter a requied date for when this event starts.")
	#starttime = models.TimeField(blank=True, null=True, help_text="Enter an option 24-hour time for when this event starts.")
	#enddate = models.DateField(help_text="Enter a requied date for when this event ends.")
	#endtime = models.TimeField(blank=True, null=True, help_text="Enter an option 24-hour time for when this event ends.")
	event_type = models.CharField(max_length=1, blank=False, null=False, choices=TYPES)
	title = models.CharField(max_length=200, help_text="Enter the title for this event (e.g. Diabetes Lecture).")
	short_description = models.CharField(max_length=300, help_text="Enter a short description for this event.")
	description = models.TextField(help_text="Enter a description for this event.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	service = models.ForeignKey(Service, blank=True, null=True, help_text="Select the Specialty or Service associated with this event, if any.")
	related_services = models.ManyToManyField(Service, blank=True, null=True, related_name='s_related', help_text="Select optional related services for this event.")
	local_presenters = models.ManyToManyField(Doctor, blank=True, help_text="Select the SMG professionals presenting this event, if any.")
	other_presenter = models.CharField(max_length=200, blank=True, help_text="Enter another presenter nome for this event.")
	presenter_url = models.URLField(max_length=500, blank=True, help_text="Enter a URL reference for the other presenter above, if applicable.")
	sponsored_by = models.CharField(max_length=200, blank=True, help_text="Enter on optional sponsored-by line.")
	sponsor_url = models.URLField(max_length=500, blank=True, help_text="Enter a URL reference for the sponsor, if applicable.")
	location = models.ForeignKey(Location, blank=True, null=True, default=18, help_text="Select a location at SMG.")
	room = models.CharField(max_length=100, blank=True, default="Conference Center", help_text="Enter a room at this location.")
	other_location = models.TextField(blank=True, help_text="If this event is not at SMG, leave the above information blank and enter an address and parking information here.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/event-images', help_text="Upload an image for this event. This image will automatically be scaled to no greater than %sx%s for display on the site." % (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/event-images')
	icon = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/event-images', help_text="Upload an icon for this event. This icon will be displayed next to the event on the homepage. This image will automatically be scaled to %sx%s for display on the site." % (ICON_MAX_WIDTH, ICON_MAX_HEIGHT))
	date_added = models.DateField(auto_now_add=True)
	exclude_from_registration = models.CharField(max_length=1, default=u'0', choices=cms.Model.EXCLUDE, help_text="Select Exclude to exclude this event from registration.")
	notification = models.TextField(blank=True, help_text="Enter a notification to be emailed to all registered users of this event. Emails are sent whenever changes to this field are confirmed in the CMS.")
	
	class Meta:
		ordering = ['title']
	
	def __unicode__(self):
		return self.title
	
	def save(self, preview=True):
		if not preview and whitespace_re.match(self.notification) and self.notification != Event.all_objects.get(id=self.id).notification:
			self.notify()
		super(Event, self).save(preview)
	
	def notify(self):
		import smtplib
		import os, sys
		accounts = Registration.objects.filter(eventtimes__event=self)
		for account in accounts:
			toaddrs  = (account.email,)
			fromaddr = 'events@summitmedicalgroup.com'
			msg = 'From: \'Summit Medical Group Event Hotline\' <events@summitmedicalgroup.com>\r\n'
			msg = 'Reply-To: \'Summit Medical Group Event Hotline\' <events@smgnj.com>\r\n'
			msg += 'To: %s\r\n' % account.email
			msg += 'Subject: Important Update re: your Summit Medical Group event registration\r\n\r\n'
			msg += 'Dear %s %s: \r\n\r\n' % (account.first_name, account.last_name)
			msg += self.notification
			msg += '\r\n\r\nThank you,\r\n'
			msg += 'Summit Medical Group\r\n\r\n'

			try:
				server = smtplib.SMTP('localhost')
				server.set_debuglevel(1)
				server.sendmail(fromaddr, toaddrs, msg)
				server.quit()
				account.status = 'C'
				account.save()
			except:
				print 'Unable to send messages to %s because %s' % (toaddrs, sys.exc_info()[0])
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)

	def expired(self):
		if self.enddate < date.today():
			return True
		return False

	def presenter(self):
		presenter = False
		if self.local_presenters.count() > 0 or self.other_presenter:
			presenter = True
		return presenter

	def multiple_sponsers(self):
		multiple = False
		if self.local_presenters.count() > 1 or (self.local_presenters.count() == 1 and self.other_presenter):
			multiple = True
		return multiple

	def firstdate(self):
		eventtimes = self.eventtime_set.order_by('startdate', 'starttime')
		if eventtimes:
			return eventtimes[0].startdate
		return None

	def registered(self):
		count = 0
		for eventtime in self.eventtime_set.all():
			count += len(eventtime.registration_set.all())
		return count

	def eventtimes(self):
		eventtimes = Eventtime.objects.filter(event=self, startdate__gte=date.today()).order_by('startdate', 'starttime')
		finallist = []
		for eventtime in eventtimes:
			if eventtime.event.active == u'1' and eventtime.event.for_update <= 1:
				finallist.append(eventtime)
		return finallist

	def most_recent(self):
		eventtimes = Eventtime.objects.filter(event=self, startdate__gte=date.today()).order_by('startdate', 'starttime')
		if eventtimes:
			return eventtimes[0]
			return eventtimes[0].event.timelong()
		return "None or before today"

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s %s %s" % (self.title, self.description, self.local_presenters, self.other_presenter)
		return SearchKey(self.pk, self.get_absolute_url(), self.firstdate(), self.title, self.title, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.firstdate(), self.title, self.keywords, self.keywords)


class Referrer(models.Model):
	"""
	Model to store referrer options for event registrations.
	"""
	name = models.CharField(max_length=75, help_text="Enter a name for the referrer list for event registrations.")
	order = models.PositiveSmallIntegerField(default=1, help_text="Enter the numebr of the order for this item to appear in the list.")
	def __unicode__(self):
		return u'%s' % self.name
	class Admin:
		list_display = ('name', 'order')
		ordering = ('order',)


class Registration(models.Model):
	"""
	Model to store user registrations for events.
	"""
	
	STATES = (
		('CT', 'Connecticut'),
		('DE', 'Delaware'),
		('NJ', 'New Jersey'),
		('NY', 'New York'),
		('PA', 'Pennsylvania')
	)
	
	MAIL = (
		('T', 'Yes'),
		('F', 'No')
	)
	
	STATUS = (
		('N', 'New registration'),
		('C', 'Sent confirmation'),
		('R', 'Sent reminder')
	)
	
	ENTERED = (
		('U', 'User'),
		('A', 'Admin')
	)
	
	signup_date = models.DateTimeField(auto_now_add=True)
	entered_by = models.CharField(max_length=1, choices=ENTERED, default='A')
	#events = models.ManyToManyField(Event)
	eventtimes = models.ManyToManyField('Eventtime')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	age = models.IntegerField(null=True)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=STATES, default='NJ')
	zipcode = models.CharField(max_length=10)
	email = models.EmailField()
	main_phone = models.CharField(max_length=20)
	alt_phone = models.CharField(max_length=20, blank=True)
	referrer = models.ForeignKey(Referrer)
	sendmail = models.CharField(max_length=1, choices=MAIL, default='T', help_text="Send group emails to this user?")
	#guests = models.PositiveSmallIntegerField(default=0)
	status = models.CharField(max_length=1, choices=STATUS, default='N', help_text="Choose 'New registration' to send confirmation and reminder emails, or choose 'Sent reminder' to not send any emails to this user.")
	
	class Meta:
		verbose_name = 'Event Registrations'
		verbose_name_plural = 'Event Registrations'


class EventBanner(cms.Model, models.Model):
	"""
	Model for holding Event Banner images

	Height and width fields are prepopulated with our standard,
	but not enforced by the model.
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Only one Event Banner can be active. If you set this Event Banner to be active, it will deactivate any other event currently set to active.")
	name = models.CharField(max_length=50, help_text="Please enter a name for this Event Banner.")
	image = models.ImageField(width_field='', height_field='', upload_to='db/event_banners/%Y/%m/%d')
	date_added = models.DateField(auto_now_add=True)
	link = models.ForeignKey(Event, blank=True, null=True, help_text="Select the event that this banner links to.")

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Event Banner"
		verbose_name_plural = "Event Banners"

	def save(self, preview=True, recurse=False):
		if self.active == u'1' and not preview and not recurse:
			for e in EventBanner.objects.all():
				e.active = u'0'
				e.save(preview=False, recurse=True)
			self.active = u'1'
		super(EventBanner, self).save(preview=preview)

	def get_url(self):
		try:
			return self.link.get_absolute_url()
		except Event.DoesNotExist:
			return '/events/'


class Class(cms.Model, search.Model, models.Model, cms.ClonableMixin):
	"""
	Model for Classes

	This is a model for the classes entered and displayed on the website.
	"""

	qa_objects = cms.QAManager()
	objects = ClassManager()
	all_objects = models.Manager()
	display_objects = EventDisplayManager()
	item_url = 'class'
	search_order = 4
	search_limit = 10

	ONDAY = (
			(u'1', 'Held this day'),
			(u'0', 'Not held'),
			)

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this class from display and search on the site.")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Aerobics-Class' to have this Class load at '/class/Aerobics-Class/'). This is normally created for you from the title.")
	startdate = models.DateField(help_text="Enter a requied date for when this class starts.")
	starttime = models.TimeField(blank=True, null=True, help_text="Enter an optional 24-hour time for when this class starts.")
	enddate = models.DateField(blank=True, null=True, help_text="Enter a date for when this event ends.")
	endtime = models.TimeField(blank=True, null=True, help_text="Enter an optional 24-hour time for when this class ends.")
	cancellations = models.TextField(blank=True, help_text="Enter cancellation dates or other urgent information about this class.")
	days = models.CharField(max_length=7, help_text="Select the days when the class takes place.")
	monday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	tuesday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	wednesday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	thursday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	friday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	saturday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	sunday = models.CharField(max_length=1, default=u'0', choices=ONDAY)
	title = models.CharField(max_length=200, help_text="Enter the title for this class (e.g. Aerobics Class).")
	short_description = models.CharField(max_length=300, help_text="Enter a short description for this class.")
	description	= models.TextField(help_text="Enter a description for this class.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	service = models.ForeignKey(Service, blank=True, null=True, help_text="Select the Specialty or Service associated with this class, if any.")
	related_services = models.ManyToManyField(Service, blank=True, null=True, related_name='class_s_related', help_text="Select optional related services for this class.")
	local_presenters = models.ManyToManyField(Doctor, blank=True, help_text="Select the SMG professionals presenting this class, if any.")
	other_presenter = models.CharField(max_length=200, blank=True, help_text="Enter another presenter nome for this class.")
	presenter_url = models.URLField(max_length=500, blank=True, help_text="Enter a URL reference for the other presenter above, if applicable.")
	sponsored_by = models.CharField(max_length=200, blank=True, help_text="Enter on optional sponsored-by line.")
	sponsor_url = models.URLField(max_length=500, blank=True, help_text="Enter a URL reference for the sponsor, if applicable.")
	location = models.ForeignKey(Location, blank=True, null=True, default=18, help_text="Select a location at SMG.")
	room = models.CharField(max_length=100, blank=True, default="Conference Center", help_text="Enter a room at this location.")
	other_location = models.TextField(blank=True, help_text="If this class is not at SMG, leave the above information blank and enter an address and parking information here.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/class-images', help_text="Upload an image for this class. This image will automatically be scaled to no greater than %sx%s for display on the site." % (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/class-images')
	icon = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/class-images', help_text="Upload an icon for this class. This icon will be displayed next to the class on the homepage. This image will automatically be scaled to %sx%s for display on the site." % (ICON_MAX_WIDTH, ICON_MAX_HEIGHT))
	date_added = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name = 'Class'
		verbose_name_plural = 'Classes'
		ordering = ['-startdate', '-starttime']

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
		
	def days_held(self):
		days = []
		if self.monday == '1': days.append('Mondays')
		if self.tuesday == '1': days.append('Tuesdays')
		if self.wednesday == '1': days.append('Wednesdays')
		if self.thursday == '1': days.append('Thursdays')
		if self.friday == '1': days.append('Fridays')
		if self.saturday == '1': days.append('Saturdays')
		if self.sunday == '1': days.append('Sundays')
		return days
		
	def starttime_display(self):
		return self.starttime.strftime('%I:%M %p')
		

	def timelong(self):
		if self.startdate == self.enddate:
			if not self.starttime and not self.endtime:
				val = u'%s' % (self.startdate.strftime('%A, %B %d, %Y'))
			elif not self.starttime:
				val = u'%s, - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.endtime.strftime('%I:%M %p'))			
			else:
				val = u'%s, %s - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.starttime.strftime('%I:%M %p'), self.endtime.strftime('%I:%M %p'))
		elif not self.endtime or not self.enddate:
			val = u'%s, %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.starttime.strftime('%I:%M %p'))
		else:
			val = u'%s - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.enddate.strftime('%A, %B %d, %Y'))
		return zero_re.sub(' \\1', val)

	def timeshort(self):
		if self.startdate == self.enddate:
			if not self.starttime:
				val = u'%s' % (self.startdate.strftime('%a., %b. %d'))
			else:
				val = u'%s, %s' % (self.startdate.strftime('%a., %b. %d'), self.starttime.strftime('%I:%M %p'))
		elif not self.endtime or not self.enddate:
			val = u'%s, %s' % (self.startdate.strftime('%a., %b. %d'), self.starttime.strftime('%I:%M %p'))
		else:
			val = u'%s - %s' % (self.startdate.strftime('%a., %b. %d'), self.enddate.strftime('%a., %b. %d'))
		return zero_re.sub(' \\1', val)

	def expired(self):
		if self.enddate < date.today():
			return True
		return False

	def presenter(self):
		presenter = False
		if self.local_presenters.count() > 0 or self.other_presenter:
			presenter = True
		return presenter

	def multiple_sponsers(self):
		multiple = False
		if self.local_presenters.count() > 1 or (self.local_presenters.count() == 1 and self.other_presenter):
			multiple = True
		return multiple

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s %s %s" % (self.title, self.description, self.local_presenters, self.other_presenter)
		return SearchKey(self.pk, self.get_absolute_url(), self.startdate, self.title, self.title, body)

	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.startdate, self.title, self.keywords, self.keywords)


class Eventtime(cms.Model, models.Model):
	"""
	Model for Event times
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	CANCELLED = (
		('A', 'Active'),
		('C', 'Cancelled')
	)

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")
	event = models.ForeignKey(Event)
	startdate = models.DateField(help_text="Enter a requied date for when this event starts.")
	starttime = models.TimeField(blank=True, null=True, help_text="Enter an option 24-hour time for when this event starts.")
	enddate = models.DateField(help_text="Enter a requied date for when this event ends.")
	endtime = models.TimeField(blank=True, null=True, help_text="Enter an option 24-hour time for when this event ends.")
	cancelled = models.CharField(max_length=1, choices=CANCELLED, default='A', help_text="Cancel this event?")

	def __unicode__(self):
		return u"%s: %s -- %s to %s -- %s" % (self.event.title, self.startdate, self.starttime, self.enddate, self.endtime)

	def timelong(self):
		if self.startdate == self.enddate:
			if not self.starttime and not self.endtime:
				val = u'%s' % (self.startdate.strftime('%A, %B %d, %Y'))
			elif not self.starttime:
				val = u'%s, - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.endtime.strftime('%I:%M %p'))
			elif not self.endtime:
				val = u'%s, %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.starttime.strftime('%I:%M %p'))
			else:
				val = u'%s, %s - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.starttime.strftime('%I:%M %p'), self.endtime.strftime('%I:%M %p'))
		else:
			val = u'%s - %s' % (self.startdate.strftime('%A, %B %d, %Y'), self.enddate.strftime('%A, %B %d, %Y'))
		return zero_re.sub(' \\1', val)

	def timeshort(self):
		if self.startdate == self.enddate:
			if not self.starttime:
				val = u'%s' % (self.startdate.strftime('%a., %b. %d'))
			else:
				val = u'%s, %s' % (self.startdate.strftime('%a., %b. %d'), self.starttime.strftime('%I:%M %p'))
		else:
			val = u'%s - %s' % (self.startdate.strftime('%a., %b. %d'), self.enddate.strftime('%a., %b. %d'))
		return zero_re.sub(' \\1', val)

	def expired(self):
		if self.enddate < date.today():
			return True
		return False

