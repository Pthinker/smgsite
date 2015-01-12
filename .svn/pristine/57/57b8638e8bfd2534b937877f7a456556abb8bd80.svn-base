from django.db import models
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import get_script_prefix

import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.marketing_banners.models import MarketingBanner
from smgsite.search.containers import SearchKey

class Template(models.Model):
	"""
	Model for registering templates used to display custom pages.
	"""
	name = models.CharField(max_length=50, help_text="Enter the name of this template (e.g. enter 'services/cardiology.html' if this template is on disk at 'templates/pages/services/cardiology.html') All page templates reside under 'templates/pages'.")
	
	def __unicode__(self):
		return u'%s' % self.name


class Directory(models.Model):
	"""
	Model for directories under which custom Pages can be added.
	"""
	directory = models.CharField(max_length=100, help_text="Enter the path of this directory (e.g. enter '/service/cardiology/' to create a directory so custom pages can be added whithin it.")
	template = models.ForeignKey(Template, help_text="Select the template to be used for all pages created in this directory.")
	
	class Meta:
		ordering = ['directory']
		verbose_name_plural = "Directories"
	
	def __unicode__(self):
		return u'%s' % self.directory
	
	def save(self):
		self.directory = self.directory.strip('/')
		super(Directory, self).save()


class Page(cms.Model, search.Model, models.Model):
	"""
	Model for CMS controlled custom pages on the site.
	"""
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	search_order = 8
	search_limit = 10
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, 
		help_text="Select Inactive to remove this page from display and search on the site.")
	directory = models.ForeignKey(Directory, blank=True, null=True)
	urlname = models.CharField(max_length=50, blank=True, 
		help_text="Enter end of URL (e.g. enter 'aboutus' to have this Service load at '/aboutus/'). This Urlname is appended to the Directory above to create the complete path. It is not necessary to enter / characters.")
	keywords = models.CharField(max_length=500, blank=True, 
		help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, 
		help_text="Enter an optional meta description for SEO.")
	title = models.CharField(max_length=100, 
		help_text="Enter the title of this page.")
	content = models.TextField(blank=True)
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="pages_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	
	url = models.CharField('URL', blank=True, max_length=100,
		help_text="Enter URL path for this page. Example: /help/faq/")
	template_name = models.CharField('Template', max_length=70, blank=True,
        help_text="Select a template. If this isn't provided, the system will use 'default.html'.")

	class Meta:
		verbose_name = 'Summit Medical Group Pages'
		verbose_name_plural = 'Summit Medical Group Pages'
	
	def __unicode__(self):
		return self.title
	
	def get_absolute_url(self):
		if self.urlname:
			return "/%s/%s/" % (self.directory, self.urlname)
		else:
			return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
	
	def cms_directory_id_display(self, directory_id):
		if self.directory:
			try:
				return Directory.objects.get(pk=directory_id).directory
			except:
				return '(none)'
		else:
			return '(none)'
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s" % (self.title, self.content)
		return SearchKey(self.pk, self.get_absolute_url(), self.title, self.title, self.title, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.title, self.title, self.keywords, self.keywords)




