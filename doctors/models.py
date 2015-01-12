import time
from datetime import datetime

from django.db import models
from django import forms
from django.db.models import Q
from django.core.cache import cache
from django.templatetags.static import static

from smgsite.settings import MEDIA_URL
import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.search.containers import SearchKey
import smgsite.site.models as site
from smgsite.services.models import Service
from smgsite.site import image_make_thumbnail
from smgsite.blogs.models import Blog, BlogEntry
from smgsite.marketing_banners.models import MarketingBanner

IMAGE_MAX_WIDTH = 140
IMAGE_MAX_HEIGHT = 196

THUMBNAIL_MAX_WIDTH = 100
THUMBNAIL_MAX_HEIGHT = 140


class Hospital(models.Model):
	"""
	A model to facilitate multiple hostpial selections per doctor
	"""
	hospital = models.CharField(max_length=100)
	hospital_url = models.URLField(max_length=500, blank=True, help_text="Enter a URL link for the hospital, if applicable.")

	def __unicode__(self):
		return u'%s' % self.hospital

	class Meta:
		ordering = ['hospital']

	def save(self):
		super(Hospital, self).save()
		cache.delete('finder-hospitals')
		cache.delete('finder-hospitals-list')


class Language(models.Model):
	"""
	A model to facilitate multiple hostpial selections per doctor
	"""
	language = models.CharField(max_length=50)

	def __unicode__(self):
		return u'%s' % self.language

	class Meta:
		ordering = ['language']

	def save(self):
		super(Language, self).save()
		cache.delete('finder-languages')
		cache.delete('finder-languages-list')


class Specialty(cms.Model, search.Model, models.Model):
	"""
	Model for doctor specialties
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'specialty'
	search_order = 3
	search_limit = 10


	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this specialty from display and search on the site.")
	specialty = models.CharField(max_length=100, unique=True, help_text="Enter the name of the specialty.")

	class Meta:
		ordering = ['specialty']
		verbose_name_plural = "Specialties"

	def __unicode__(self):
		return u'%s' % self.specialty

	def get_absolute_url(self):
		return "/doctor-specialty?search-input=%s" % self.specialty

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.specialty, self.specialty, self.specialty, self.specialty)
	
	def name(self):
		return self.specialty

class SpecialtyUpdate(models.Model):
	"""
	Temporary model for doctor specialty updates
	"""

	doctor = models.ForeignKey('Doctor')
	specialty = models.CharField(max_length=100, help_text="Enter the name of the specialty.")

	class Meta:
		ordering = ['specialty']
		verbose_name_plural = "Specialties"

	def __unicode__(self):
		return u'%s' % self.specialty

	def quoted(self):
		return u'%s' % self.specialty.replace('"', '""')


class Doctor(cms.Model, search.Model, models.Model):
	"""
	Model for Doctor information
	
	# ***Unit testing to ensure uniqueness constraints are obeyed***
	>>> from smgsite.doctors.models import Doctor
	>>> doctor = Doctor.objects.create(first_name="A", last_name="Test", urlname="test1", email="test1", phone='11')
	>>> doctor2 = Doctor.objects.create(first_name="A", last_name="Test2", urlname="test2", email="test2", phone='11')
	>>> doctor3 = Doctor.objects.create(first_name="A", last_name="Test3", urlname="test1", email="test3", phone='11')
	Traceback (most recent call last):
		...
    IntegrityError: (1062, "Duplicate entry 'test1' for key 2")
	>>> doctor4 = Doctor.objects.create(first_name="A", last_name="Test4", urlname="test4", email="test1", phone='11')
	Traceback (most recent call last):
		...
    IntegrityError: (1062, "Duplicate entry 'test1' for key 3")
	>>> doctor4.delete()
	Traceback (most recent call last):
		...
	NameError: name 'doctor4' is not defined
	>>> doctor3.delete()
	Traceback (most recent call last):
		...
	NameError: name 'doctor3' is not defined
	>>> doctor2.delete()
	>>> doctor.delete()
	
	# ***Unit testing for fields and search -- ensures created fields are returned for the search index***
	>>> from smgsite.doctors.models import Doctor
	>>> doctor = Doctor.objects.create(first_name="A", last_name="Test", urlname="test", email="test", phone='11')
	>>> doctor.services.create(name="Slicing", urlname="slicing")
	<Service: Slicing>
	>>> doctor.services.create(name="Dicing", urlname="dicing")
	<Service: Dicing>
	>>> index = doctor.search_index()
	>>> index
	(3L, '/doctor/test/', 'Test', 'A  Test ', 'A Test', 'A  Test  Dicing Slicing ')
	
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'doctor'
	search_order = 1
	search_limit = 10
	
	STATUS = (
		('D', 'Doctor'),
		('S', 'Staff'),
	)

	ACCEPTING = (
		('A', 'Accepting'),
		('P', 'No PCP'),
		('N', 'Not Accepting'),
	)

	GENDER = (
		('F', 'Female'),
		('M', 'Male'),
	)

	PARTICIPATE = (
		('P', 'Participates in athenahealth'),
		('D', 'Does not participate'),
		('M', 'Participates in Paramount'),
	)

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this person from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for URL (e.g. enter 'jsmith' to have this Doctor load at '/doctor/jsmith/')")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	seo_keywords = models.TextField(blank=True, help_text="Enter optional keywords for SEO. These are not used for site search.")
	prefix = models.CharField(max_length=5, blank=True, help_text="Enter name prefix (e.g. Dr.) or leave blank.")
	first_name = models.CharField(max_length=25, help_text="Enter first name.")
	middle_name = models.CharField(max_length=25, blank=True, help_text="Enter middle name or initial.")
	last_name = models.CharField(max_length=25, help_text="Enter last name.")
	gender = models.CharField(max_length=1, choices=GENDER)
	suffix = models.CharField(max_length=25, blank=True, help_text="Enter suffic (e.g. Jr. or III)")
	letters = models.CharField(max_length=50, help_text="Enter accreditation letters for name display, without periods (e.g. MD, FACP).")
	email = models.EmailField(unique=True, help_text="Enter email address, usually first initial last name @smgnj.com (e.g. avinod@smgnj.com).")
	phone = models.CharField(max_length=100, help_text="Enter phone number.")
	phone_note = models.CharField(max_length=500, blank=True, help_text="Enter phone notes.")
	#fax = models.CharField(max_length=19, blank=True, help_text="Enter fax number or leave blank.")
	#location = models.ForeignKey(site.Location, blank=True, null=True, help_text="Select a location for this person.")
	#extra_locations = models.ManyToManyField(site.Location, blank=True, related_name='extra_locations', help_text="Select any additional locations for this praticioner.")
	hospitals = models.ManyToManyField(Hospital, blank=True, help_text="Select any number of hospital locations for this practitioner.")
	languages = models.ManyToManyField(Language, default="English", help_text="Select the languages spoken by this practitioner.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/doctor-images', help_text="Upload an image for this doctor. This image will automatically be scaled to two versions, %sx%s and %sx%s" % (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT, THUMBNAIL_MAX_WIDTH, THUMBNAIL_MAX_HEIGHT))
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/doctor-images')
	thumbnail = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/doctor-images')
	cropped_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/doctor-images', help_text="Upload a cropped image for this doctor. This image will be used for the flyover on the doctors index page.")
	date_added = models.DateField(auto_now_add=True)
	title_service = models.ForeignKey(Service, related_name="title_service", null=True, help_text="Enter the primary specialty for this person, which will display on the Doctor listing page.")
	services = models.ManyToManyField(Service, related_name="services", blank=True, null=True, help_text="Enter any additional specialties for this person. The primary specialty should not be selected again.")
	touch = models.TextField(blank=True, help_text="Enter optional personal touch content for this doctor.")
	exclude_from_index = models.CharField(max_length=1, default=u'0', choices=cms.Model.EXCLUDE, help_text="Select Exclude to remove this person from listing in the main doctors index pages.")
	blog = models.ForeignKey(Blog, blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS, default='D', help_text="Selected if this entry is for a doctor or a staff member.")
	
	accepting_flag = models.CharField(max_length=1, default='A', choices=ACCEPTING, 
		help_text="Select whether this doctor is currently accepting new patients.")
	accepting = models.TextField(blank=True, 
		help_text="Enter optional text describing whether this doctor is currently accepting new patients.")
	# patient portal flags
	patient_portal = models.CharField(max_length=200, blank=True, help_text="Enter a URL for this doctor's patient portal.")
	appointments = models.CharField(max_length=1, default=u'P', choices=PARTICIPATE, help_text="Select Participates if this doctor participates in the Appointments feature.")
	portal_refill = models.CharField(max_length=1, default=u'P', choices=PARTICIPATE, help_text="Select Participates if this doctor participates in the E-mail doctor feature.")
	email_staff = models.CharField(max_length=1, default=u'P', choices=PARTICIPATE, help_text="Select Participates if this doctor participates in the E-mail staff feature.")
	lab_results = models.CharField(max_length=1, default=u'P', choices=PARTICIPATE, help_text="Select Participates if this doctor participates in the Lab results feature.")
	portal_accounts = models.CharField(max_length=1, default=u'P', choices=PARTICIPATE, help_text="Select Participates if this doctor participates in the Personal Health Records feature.")
	
	specialties = models.ManyToManyField(Specialty, blank=True, help_text="Select any number of specialties for this practitioner.")
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="doctors_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	
	class Meta:
		ordering = ['last_name']
		verbose_name_plural = "Doctors and Practitioners"
	
	def __unicode__(self):
		return self.name()
	
	def name(self):
		if self.suffix:
			name = u'%s %s %s, %s, %s' % (self.first_name, self.middle_name, self.last_name, self.suffix, self.letters)
		else:
			name = u'%s %s %s, %s' % (self.first_name, self.middle_name, self.last_name, self.letters)
		return name
	
	def display_name(self):
		if self.suffix:
			name = u'%s %s %s, %s' % (self.first_name, self.middle_name, self.last_name, self.suffix)
		else:
			name = u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)
		return name
	
	def list_name(self):
		if self.suffix:
			name = u'%s, %s %s, %s' % (self.last_name, self.first_name, self.middle_name, self.suffix)
		else:
			name = u'%s, %s %s' % (self.last_name, self.first_name, self.middle_name)
		return name
	
	def remainder_name(self):
		if self.middle_name:
			name = u'%s %s' % (self.first_name, self.middle_name)
		else:
			name = u'%s' % (self.first_name)
		if self.suffix:
			name += u', %s' % (self.suffix)
		return name
	
	def title_service_name(self):
		if self.title_service:
			return self.title_service.name
		return None

	def is_accepting(self):
		return self.accepting_flag == 'A'

	def is_unterminated(self):
		if self.accepting[-1] in ['.', '!', '?']:
			return False
		return True

	def primary_location(self):
		return self.location_set.filter(position=1)[0]

	def has_extra_locations(self):
		return len(self.location_set.filter(position__gt=1)) > 0

	def extra_locations(self):
		return self.location_set.filter(position__gt=1)

	def services_links(self):
		link = ''
		more = False
		if self.title_service:
			if self.title_service.active != u'0':
				links = '<a href="%s">%s</a>' % (self.title_service.get_absolute_url(), self.title_service.name)
			else:
				links = '%s' % (self.title_service.name)
			more = True
		for service in self.services.iterator():
			if more:
				links += '; '
			if service.active != u'0':
				links += '<a href="%s">%s</a>' % (service.get_absolute_url(), service.name)
			else:
				links += '%s' % (service.name)
			more = True
		return links
	
	def list_services(self):
		services = ''
		more = False
		if self.title_service:
			services = self.title_service.name
			more = True
		for service in self.services.iterator():
			if more:
				services += '; '
			services += service.name
			more = True
		return services

	def list_services_by_line(self):
		services = ''
		more = False
		if self.title_service:
			if self.title_service.active == '1':
				services = '<a href="{0}">{1}</a>'.format(self.title_service.get_absolute_url(), self.title_service.name)
			else:
				services = '{0}'.format(self.title_service.name)
			more = True
		for service in self.services.iterator():
			if more:
				services += '<br>'
			if service.active == '1':
				services += '<a href="{0}">{1}</a>'.format(service.get_absolute_url(), service.name)
			else:
				services += '{0}'.format(service.name)
			more = True
		return services
	
	def practitioner_name(self):
		if self.title_service:
			return self.title_service.practitioner_name
		return None
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def letter_key(self):
		return self.last_name[0]
	
	def get_degrees(self):
		if self.qa:
			degrees = self.degree_set.select_related().order_by('doctors_degree_letters.sort_order')
		else:
			degrees = self.degree_set.model.objects.filter(doctor=self).select_related().order_by('doctors_degree_letters.sort_order')
		return degrees
	
	def get_accreditations(self):		
		if hasattr(self, "qa") and self.qa:
			accreditations = self.accreditation_set.select_related().order_by('doctors_accreditation_name.sort_order')
		else:
			accreditations = self.accreditation_set.model.objects.filter(doctor=self).select_related().order_by('doctors_accreditation_name.sort_order')
		return accreditations
	
	def get_nav_links(self):
		if hasattr(self, "qa") and self.qa:
			links = self.link_nav_set.select_related().order_by('doctors_link_nav.position')
		else:
			links = self.link_nav_set.model.objects.filter(doctor=self).select_related().order_by('doctors_link_nav.position')
		return [x.resource for x in links]
        
        def get_hospitals(self):
            return self.hospitals.order_by('hospital')
        
	def blog_list(self):
		return self.blog.blogentry_set.all()[:5]
	
	# Portal links 
	def participating(self):
		return (
				self.appointments in ('P', 'M') or
				self.portal_refill in ('P', 'M') or 
				self.email_staff in ('P', 'M') or 
				self.lab_results in ('P', 'M') or 
				self.portal_accounts in ('P', 'M'))

	@property
	def get_portal_url(self):
		if self.patient_portal:
			return self.patient_portal
		else:
			return '/about/MySMG/'

	def has_portal_refill(self):
		if self.portal_refill in ('P', 'M'):
			return self.get_portal_url
		return False

	def has_email_staff(self):
		if self.email_staff in ('P', 'M'):
			return self.get_portal_url
		return False

	def has_appointments(self):
		if self.appointments in ('P', 'M'):
			return self.get_portal_url
		return False

	def has_lab_results(self):
		if self.lab_results in ('P', 'M'):
			return self.get_portal_url
		return False
	
	def has_portal_accounts(self):
		if self.portal_accounts in ('P', 'M'):
			return self.get_portal_url
		return False


	def pkstr(self):
		return u'%s' % self.pk
	
	def save(self, preview=True):
		super(Doctor, self).save(preview)
		cache.delete('finder-doctor-locations')
		cache.delete('finder-doctor-services-%s' % self.id)
		cache.delete('finder-doctor-specialty')
		cache.delete('finder-doctor-hospitals-%s' % self.id)
		cache.delete('finder-doctor-hospitals')
		cache.delete('finder-doctor-languages')
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s " % self.name()
		topbody = "%s " % self.name()
		body += "%s " % unicode(self.title_service)
		topbody += "%s " % unicode(self.title_service)
		for service in self.services.all():
			body += "%s " % unicode(service)
		for degree in self.degree_set.all():
			body += "%s %s " % (degree.letters.letters, degree.description)
		for accreditation in self.accreditation_set.all():
			body += "%s %s " % (accreditation.name.name, accreditation.description)
		for specialty in self.specialties.all():
			body += "%s " % (specialty.specialty)
		body += "%s " % unicode(self.touch)
		if self.suffix:
			display = '<a href="%s">%s, %s %s, %s, <span class="doctor_cred">%s</span></a> - <span class="doctor_dept">%s</span>' % (self.get_absolute_url(), self.last_name, self.first_name, self.middle_name, self.suffix, self.letters, self.list_services())
		else:
			display = '<a href="%s">%s, %s %s, <span class="doctor_cred">%s</span></a> - <span class="doctor_dept">%s</span>' % (self.get_absolute_url(), self.last_name, self.first_name, self.middle_name, self.letters, self.list_services())
		return SearchKey(self.pk, self.get_absolute_url(), self.last_name, display, topbody, body)
	
	def keyword_index(self):
		if self.suffix:
			display = '<a href="%s">%s, %s %s, %s, <span class="doctor_cred">%s</span></a> - <span class="doctor_dept">%s</span>' % (self.get_absolute_url(), self.last_name, self.first_name, self.middle_name, self.suffix, self.letters, self.list_services())
		else:
			display = '<a href="%s">%s, %s %s, <span class="doctor_cred">%s</span></a> - <span class="doctor_dept">%s</span>' % (self.get_absolute_url(), self.last_name, self.first_name, self.middle_name, self.letters, self.list_services())
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.last_name, display, self.keywords, self.keywords)

	def display_image(self):
		if self.original_image:
			return self.original_image
		else:
			return static('images/no_doc_image.png')


class Degree_letters(models.Model):
	"""
	Model for degree letters
	"""
	
	letters = models.CharField(max_length=8)
	sort_order = models.PositiveSmallIntegerField(default=0)
	description_short = models.CharField(max_length=100, blank=True)
	description_long = models.TextField(blank=True)
	
	class Meta:
		verbose_name = 'Degree letters'
		verbose_name_plural = 'Degree letters'
	
	def __unicode__(self):
		return self.letters


class Degree(cms.Model, models.Model):
	"""
	Model for Doctor degrees
	
	Examples include:
	BS: Fairleigh Dickinson University, New Jersey; 1990
	DO: New York College of Osteopathic Medicine, New York
	DPM: Cum Laude, New York College of Podiatric Medicine, New York, NY. June 2004
	
	Has a one-to-many relationship to doctors:
	each doctor can have zero or more degrees.
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	qa = False # Secret QA flag
	
	parent = 'doctor'
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")	
	doctor = models.ForeignKey(Doctor)
	letters = models.ForeignKey(Degree_letters)
	description = models.CharField(max_length=300, help_text="Enter description (e.g. 'University of Pennsylvania, Pennsylvania; 1973').")
	
	def __unicode__(self):
		return u"%s %s" % (self.letters, self.description)
	
	class Meta:
		pass


class Accreditation_name(models.Model):
	"""
	Model for names of accreditations
	"""
	
	name = models.CharField(max_length=50)
	name_plural = models.CharField(max_length=50)
	sort_order = models.PositiveSmallIntegerField(default=0)
		
	class Meta:
		verbose_name = 'Accreditation names'
		verbose_name_plural = 'Accreditation names'
	
	class Admin:
		list_display = ('name', 'sort_order')
	
	def __unicode__(self):
		return self.name


class Accreditation(cms.Model, models.Model):
	"""
	Model for Doctor accreditations, including residencies, fellowships, and board certifications.
	
	Examples include:
	Residency: Internal Medicine/Primary Care, Columbia Presbyterian Medical Center, New York, NY, 1997-2000
	Board Certification: Licensed Psychologist; Cognitive Therapist, American Academy of Cognitive Therapy
	
	Has a one-to-many relationship to doctors:
	each doctor can have zero or more accreditation entries.
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()	
	parent = 'doctor'
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")
	doctor = models.ForeignKey(Doctor)
	name = models.ForeignKey(Accreditation_name)
	description = models.CharField(max_length=300, help_text="Enter description (e.g. 'Licensed Psychologist; Cognitive Therapist, American Academy of Cognitive Therapy').")
			
	class Meta:
		pass
	
	def __unicode__(self):
		return u"%s %s" % (self.name, self.description)


class Link_Nav(cms.Model, models.Model):
	"""
	Model for resource links associated with this doctor
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")	
	resource = models.ForeignKey(site.Resource, related_name='doctor_resource_nav')
	doctor = models.ForeignKey(Doctor)
	position = models.PositiveSmallIntegerField(max_length=2)
	
	class Meta:
		ordering = ['resource']
		verbose_name = "Link for nav display"
		verbose_name_plural = "Links for nav display"
	
	def __unicode__(self):
		return u'%s (%s)' % (self.doctor, self.resource)


class Featured(cms.Model, models.Model):
	"""
	Model for featured "doctor of the week" practitioners
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")	
	doctor = models.ForeignKey(Doctor)
	startdate = models.DateField(help_text="Enter a requied date for when to start featuring this practitioner. Dates are inclusive, so a date range of 5-10 would start on the 5th and run through and including the 10th.")
	enddate = models.DateField(help_text="Enter a requied date after which to stop featuring this practitioner.")
	blurb = models.TextField(help_text="Enter text to display with this featured practitioner.")
	
	class Meta:
		ordering = ['startdate', 'enddate']
		verbose_name = "Featured Practitioner"
		verbose_name_plural = "Featured Practitioners"
	
	def __unicode__(self):
		return u'%s' % (self.doctor)

	def startdate_display(self):
		return u'%s' % self.startdate.strftime('%m-%d-%Y')
	
	def enddate_display(self):
		return u'%s' % self.enddate.strftime('%m-%d-%Y')

	def save(self, preview=True):
		start = self.startdate
		if self.startdate.__class__ == unicode:
			start = datetime(*time.strptime(self.startdate, '%Y-%m-%d')[0:5]).date()
		end = self.enddate
		print start.__class__
		if self.enddate.__class__ == unicode:
			end = datetime(*time.strptime(self.enddate, '%Y-%m-%d')[0:5]).date()
		print end.__class__
		if start > end:
			raise forms.ValidationError('The date range you selected has a start date after the end date. Please go back and correct the dates.')
		existing = Featured.all_objects.filter(Q(startdate__gte=self.startdate, startdate__lte=self.enddate) | Q(enddate__gte=self.startdate, enddate__lte=self.enddate)).exclude(pk=self.pk)
		if existing:
			raise forms.ValidationError('The date range you entered conflicts with another pracitioner who is already being fetured during this period. Please adjust the date range or review the dates for the featured practitioner %s.' % (existing[0]))
		else:
			super(Featured, self).save(preview)


class Location(cms.Model, models.Model):
	"""
	Model for Doctor locations
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")
	doctor = models.ForeignKey(Doctor)
	location = models.ForeignKey(site.Location, related_name="doctors_location")
	position = models.PositiveSmallIntegerField(default=1, help_text="Enter a number to set the order for this location on display pages. Smaller numbers appear first.")
	extra1 = models.CharField("First extra info", max_length=300, blank=True, help_text="First extra location information, displayed with the address, e.g. South Building.")
	extra2 = models.CharField("Second extra info", max_length=300, blank=True, help_text="Second extra location information, displayed with the address, e.g. Suite 200.")
	extra3 = models.CharField("Third extra info", max_length=300, blank=True, help_text="Third extra location information, displayed after the address, e.g. Use rear entrance and left elevator bank.")

	def __unicode__(self):
		return u"%s: %s -- %s -- %s" % (self.location.name, self.extra1, self.extra2, self.extra3)

