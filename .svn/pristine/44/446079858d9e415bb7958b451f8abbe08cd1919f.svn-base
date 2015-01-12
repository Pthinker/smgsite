from django.db import models
from django.template import Context, loader
from django.http import Http404
from smgsite.settings import TEMPLATE_ROOT
from smgsite.site import image_make_thumbnail
import smgsite.search.models as search
import smgsite.cms.models as cms
from smgsite.search.containers import SearchKey

THUMBNAIL_MAX_WIDTH = 100
THUMBNAIL_MAX_HEIGHT = 200

class Advisor(models.Model):
	item_url = 'library'
	name = models.CharField(max_length=50, unique=True, blank=False)
	urlname = models.CharField(max_length=100, unique=True, blank=False)
	index = models.CharField(max_length=100, unique=True, blank=False)
	code = models.CharField(max_length=3, unique=True, blank=False)
	def __unicode__(self):
		return u'%s' % (self.name)
	def get_absolute_url(self):
		return '/%s/%s/' % (self.item_url, self.urlname)


class Code(models.Model):
	code_type = models.CharField(max_length=10)
	code = models.CharField(max_length=25)
	
	class Meta:
		unique_together = ('code_type', 'code')
	
	def __unicode__(self):
		return u'%s:%s' % (self.code_type, self.code)


class Image(models.Model):
	name = models.CharField(max_length=100, unique=True)
	image = models.ImageField(width_field='', height_field='', upload_to='db/relayhealth-images')
	thumbnail = models.ImageField(width_field='', height_field='', upload_to='db/relayhealth-images')
	def save(self):
		image_make_thumbnail(self, 'image', 'thumbnail', 'db/relayhealth-images', THUMBNAIL_MAX_WIDTH, THUMBNAIL_MAX_HEIGHT)
		super(Image, self).save()


class Article(search.Model, models.Model):
	
	all_objects = models.Manager()
	objects = models.Manager()
	all_objects = models.Manager()
	item_url = 'library'
	search_order = 6
	ajax_search_limit = 5
	search_limit = 10
	
	for_update = models.PositiveSmallIntegerField(default=0, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE)
	reference = models.BooleanField(default=False)
	urlname = models.CharField(max_length=100, unique=True, editable=False)
	advisor = models.ForeignKey(Advisor)
	article_id = models.CharField(max_length=100, unique=True)
	keywords = models.CharField(max_length=2000, help_text="Enter Top Match keywords separated by spaces.")
	template = models.CharField(max_length=200, blank=False)
	title = models.CharField(max_length=200, blank=False)
	images = models.ManyToManyField(Image, blank=True, null=True)
	codes = models.ManyToManyField(Code)
	related = models.ManyToManyField('Article')
	references = models.ForeignKey('self', null=True, related_name='referencekey')
	duplicate = models.BooleanField(default=False)
	
	class Meta:
		verbose_name = 'Library Article'
		verbose_name_plural = 'Library Articles'
	
	def __unicode__(self):
		return u'%s' % self.title
	
	def letter_key(self):
		return self.title[0]
	
	def meta_description(self):
		return self.title
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def save(self, post=True):
		super(search.Model, self).save()
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		# We have to fetch the body from the file
		if self.duplicate:
			return None
		try:
			t = loader.get_template(self.template)
			body = t.render(Context())
		except loader.TemplateDoesNotExist:
			raise Http404
		return SearchKey(self.article_id, self.get_absolute_url(), self.title, self.title, self.title, body)



