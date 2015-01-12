from django.db import models
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings

from smgsite.settings import MEDIA_URL
import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.search.containers import SearchKey
import smgsite.site.models as site

from smgsite.blogs.models import Blog, BlogEntry
from smgsite.marketing_banners.models import MarketingBanner

IMAGE_MAX_WIDTH = 150
IMAGE_MAX_HEIGHT = 100

class URLAlias(cms.Model, models.Model):
	"""
	Model for URL Aliases
	"""
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this URL alias.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for this alias URL (e.g. 'cardiology')")

	class Meta:
		ordering = ['urlname']
		verbose_name = "URL Alias"
		verbose_name_plural = "URL Aliases"
	
	def __unicode__(self):
		return u'%s' % self.urlname


class Template(models.Model):
	"""
	Model for registering templates used to display service pages.
	"""
	name = models.CharField(max_length=50, help_text="Enter the name of this template (e.g. enter 'cardiology.html' if this template is on disk at 'templates/services/cardiology.html') All service templates reside under 'templates/services'.")
	
	def __unicode__(self):
		return u'%s' % self.name


class Service(cms.Model, search.Model, models.Model):
	"""
	Model for Services and Specialties
	
	This is a list of all the specialties and services at SMG.
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'service'
	template_path = 'services'
	search_order = 2
	search_limit = 10
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this service from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for URL (e.g. enter 'cardiology' to have this Service load at '/service/cardiology/').")
	template = models.ForeignKey(Template, blank=True, null=True, help_text="Select the template to be used to render this service for display.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	seo_keywords = models.TextField(blank=True, help_text="Enter optional keywords for SEO. These are not used for site search.")
	name = models.CharField(max_length=100, unique=True, help_text="Enter the full name of this service (e.g. Cardiology).")
	practitioner_name = models.CharField(max_length=100, blank=True, help_text="Enter the name of a practitoner of this service (e.g. Cardiologist).")
	practitioner_group = models.CharField(max_length=100, blank=True, help_text="Enter the group name for practitioners of this service (e.g. Our Cardiologists).")
	description_short = models.CharField(max_length=200, blank=True, help_text="A short description for this service (e.g. Heart and Blood Vessel Disorders).")
	phone = models.CharField(max_length=19, blank=True, help_text="Enter phone number.")
	#location = models.ForeignKey(site.Location, blank=True, null=True, help_text="Select a location for this service.")
	related_services = models.ManyToManyField('Service', blank=True, null=True, symmetrical=False, help_text="Select optional related services to display in the nav.")
	content = models.TextField(blank=True)
	offerings = models.TextField(blank=True)
	learn_more = models.TextField(blank=True)
	patient_tools = models.TextField(blank=True)
	#location = models.TextField(blank=True)
	#original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/service-images', help_text="Upload an image for this service. This image will automatically be scaled to no greater than %sx%s for display on the site." % (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
	#image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/service-images')
	date_added = models.DateField(auto_now_add=True)
	blog = models.ForeignKey(Blog, blank=True, null=True)
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="services_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	large_image = models.ImageField(blank=True, 
		upload_to='db/images/service', 
		help_text="Add a large image for this service.")
	small_image = models.ImageField(blank=True, 
		upload_to='db/images/service', 
		help_text="Add a small image for this service.")

	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name

	def save(self, preview=True):
		super(Service, self).save(preview)
		cache.delete('finder-services-list')
		cache.delete('finder-specialty')
	
	def get_nav_links(self):
		if hasattr(self, "qa") and self.qa:
			links = self.link_nav_set.select_related().order_by('services_link_nav.position')
		else:
			links = self.link_nav_set.model.objects.filter(service=self).select_related().order_by('services_link_nav.position')
		return [x.resource for x in links]
	
	def get_body_links(self):
		if hasattr(self, "qa") and self.qa:
			links = self.link_body_set.select_related().order_by('services_link_body.position')
		else:
			links = self.link_body_set.model.objects.filter(service=self).select_related().order_by('services_link_body.position')
		return [x.resource for x in links]
	
	"""
	The distinction between local and remote nav links has been removed from the presentation layer.
	def get_local_nav_links(self):
		if hasattr(self, "qa") and self.qa:
			links = self.link_nav_set.select_related().filter(resource__remote=False).order_by('services_link_nav.position')
		else:
			links = self.link_nav_set.model.objects.filter(service=self).select_related().filter(resource__remote=False).order_by('services_link_nav.position')
		return [x.resource for x in links]
		
	def get_remote_nav_links(self):
		if hasattr(self, "qa") and self.qa:
			links = self.link_nav_set.select_related().filter(resource__remote=True).order_by('services_link_nav.position')
		else:
			links = self.link_nav_set.model.objects.filter(service=self).select_related().filter(resource__remote=True).order_by('services_link_nav.position')
		return [x.resource for x in links]
	"""

	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def blog_list(self):
		return self.blog.blogentry_set.all()[:5]
	
	def cms_template_id_display(self, template_id):
		try:
			name = Template.objects.get(pk=template_id).name
		except Template.DoesNotExist:
			name = 'None'
		return name
	
	def letter_key(self):
		return self.name[0]
	
	def pkstr(self):
		return u'%s' % self.pk
	
	def location_plural(self):
		return len(self.location_set.filter(active='1', for_update__lte=1)) > 1

	def locations(self):
		return self.location_set.filter(active='1', for_update__lte=1).order_by('position')
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s %s %s" % (self.name, self.practitioner_name, self.practitioner_group, self.content)
		return SearchKey(self.pk, self.get_absolute_url(), self.name, self.name, self.name, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.name, self.name, self.keywords, self.keywords)

	@property
	def display_large_image(self):
		if self.large_image:
			return self.large_image
		else:
			return site.MissingImage(name='db/image-library/service_default.jpg')

	@property
	def display_small_image(self):
		if self.small_image:
			return self.small_image
		else:
			return site.MissingImage(name='db/image-library/service_default.jpg')


class ServiceGroup(cms.Model, models.Model):
	"""
	Model for Service groups
	"""
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)

	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this service from display and search on the site.")
	name = models.CharField(max_length=100)
	description = models.TextField()
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	seo_keywords = models.TextField(blank=True, help_text="Enter optional keywords for SEO. These are not used for site search.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for URL (e.g. enter 'family_health').")
	large_image = models.ImageField(upload_to='db/images/service_group', help_text="Add a large image for this group.")
	small_image = models.ImageField(upload_to='db/images/service_group', help_text="Add a small image for this group.")
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="service_group_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	order = models.PositiveIntegerField(default=0)
	services = models.ManyToManyField(Service, through='ServiceGroupDetail')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['order']

	def get_absolute_url(self):
		return '/service/group/%s/' % self.urlname
		# reverse is too fragile here because we are not using a slugfield with validation
		#return reverse('service-group', kwargs={'urlname':self.urlname})

	def list_services(self):
		services = ServiceGroupDetail.objects.filter(servicegroup=self)
		s = ['<a href="%s">%s</a>' % (s.service.get_absolute_url(), s.service.name) for s in services]
		return ', '.join(s)


class GroupDetailManager(models.Manager):
	def get_query_set(self):
		return super(GroupDetailManager, self).get_query_set().filter(service__active='1', service__for_update__lte=1)

class ServiceGroupDetail(models.Model):
	"""
	Model to link Sevices to a ServiceGroup so we can specify an order for 
	services that belong to multiple groups.
	"""
	#qa_objects = cms.QAManager()
	#objects = cms.Manager()
	#all_objects = models.Manager()

	#for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	servicegroup = models.ForeignKey(ServiceGroup)
	service = models.ForeignKey(Service)
	order = models.PositiveIntegerField(default=0, help_text='Sort order within service group')

	class Meta:
		ordering = ['order']



class Link_Nav(cms.Model, models.Model):
	"""
	Model for resource links associated with this service displayed in the nav bar
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this link from display and search on the site.")
	resource = models.ForeignKey(site.Resource, related_name='service_resource_nav')
	service = models.ForeignKey(Service)
	position = models.PositiveSmallIntegerField(max_length=2)
	
	class Meta:
		ordering = ['position']
		verbose_name = "Link for nav display"
		verbose_name_plural = "Links for nav display"
	
	def __unicode__(self):
		return u'%s (%s)' % (self.service, self.resource)


class Link_Body(cms.Model, models.Model):
	"""
	Model for resource links associated with this service displayed in the body content
	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this link from display and search on the site.")
	resource = models.ForeignKey(site.Resource, related_name='service_resource_body')
	service = models.ForeignKey(Service)
	position = models.PositiveSmallIntegerField(max_length=2)
	
	class Meta:
		ordering = ['position']
		verbose_name = "Link for content well display"
		verbose_name_plural = "Links for content well display"
	
	def __unicode__(self):
		return u'%s (%s)' % (self.service, self.resource)


class Location(cms.Model, models.Model):
	"""
	Model for Service locations
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")
	service = models.ForeignKey(Service)
	location = models.ForeignKey(site.Location, related_name="services_location")
	position = models.PositiveSmallIntegerField(default=10, help_text="Enter a number to set the order for this location on display pages. Smaller numbers appear first.")
	extra1 = models.CharField("First extra info", max_length=300, blank=True, help_text="First extra location information, displayed with the address, e.g. South Building.")
	extra2 = models.CharField("Second extra info", max_length=300, blank=True, help_text="Second extra location information, displayed with the address, e.g. Suite 200.")
	extra3 = models.CharField("Third extra info", max_length=300, blank=True, help_text="Third extra location information, displayed after the address, e.g. Use rear entrance and left elevator bank.")

	def __unicode__(self):
		return u"%d: %s -- %s -- %s" % (self.pk, self.extra1, self.extra2, self.extra3)

