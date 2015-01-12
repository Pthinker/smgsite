from django.db import models
import smgsite.cms.models as cms
import re

host_re = re.compile(r'^[\w-]+\.[\w-]+\.[\w-]+$')
site_re = re.compile(r'^[\w-]+\.[\w-]+\.[\w-]+.*$')


class Resource(models.Model):
	"""
	Model for on-site and off-site resource links.
		
	"""
	
	name = models.CharField(max_length=50, unique=True, help_text="Enter a display name for this resource.")
	description = models.CharField(max_length=200, blank=True, help_text="Enter an optional description for this resource.")
	remote = models.BooleanField(editable=False, default=False, help_text="Check this box if the URL below is outsite the SMG site.")
	url = models.CharField(max_length=200, unique=True, help_text="Enter a URL for this resource (e.g. '/service/cardiology/' or 'http://www.webmd.com/').")
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return u'%s - %s' % (self.name, self.url)
	
	def save(self):
		self.remote = False
		if host_re.match(self.url):
			self.url = 'http://%s/' % self.url
		elif site_re.match(self.url):
			self.url = 'http://%s' % self.url
		if self.url.startswith('http://'):
			self.remote = True
		super(Resource, self).save()		


class MarketingBanner(cms.Model, models.Model):
	"""
	Model for holding Marketing Banner images

	Height and width fields are prepopulated with our standard,
	but not enforced by the model.

	Each Marketing Banner may individually be activated or deactivated,
	regardless of its group membership.

	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this Marketing Banner from display on the site.")
	name = models.CharField(max_length=50, help_text="Please enter a name for this Marketing Banner.")
	image = models.ImageField(width_field='', height_field='', upload_to='db/marketing_banners/%Y/%m/%d')
	date_added = models.DateField(auto_now_add=True)
	link = models.ForeignKey(Resource, help_text="Select the resource that this banner links to.")
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name = "Marketing Banner"
		verbose_name_plural = "Marketing Banners"


class MBGroup(cms.Model, models.Model):
	"""
	Model for Marketing Banner Groups

	There is a many-to-many relationship:
	A single MarketingBanner may belong to zero or more MBGroups,
	and each MBGroup may hold zero or more MarketingBanners.

	Each MBGroup may individually be activated or deactivated,
	regardless of the settings of its member MarketingBanners.

	"""
	
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this Marketing Group from display and search on the site.")
	name = models.CharField(max_length=50, help_text="Please enter a name for this Group of Marketing Banners")
	banners = models.ManyToManyField(MarketingBanner, blank=True, null=True, verbose_name="Select a list of Marketing Banners")
	start_date = models.DateField(blank=True, null=True, help_text="You may enter an optional date on which to start display of this group.")
	end_date = models.DateField(blank=True, null=True, help_text="You may enter an option date on which to end display of this group.")
	urls = models.TextField(help_text="Enter one or more local URLs (e.g. 'service/cardiology') under which this marketing banner will be displayed. Enter one URL per line.")

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Marketing Banner Group"
		verbose_name_plural = "Marketing Banner Groups"
