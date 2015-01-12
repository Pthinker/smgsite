from django.db import models
from smgsite.settings import MEDIA_URL
import smgsite.search.models as search
import smgsite.cms.models as cms
from smgsite.search.containers import SearchKey
from datetime import datetime, timedelta


class Topic(models.Model):
	topic = models.CharField(primary_key=True, max_length=5)
	topic_name = models.CharField(max_length=100)
	
	class Meta:
		ordering = ['topic_name']
	
	def __unicode__(self):
		return u'%s' % (self.topic_name)

class Category(models.Model):
	category = models.CharField(max_length=50, help_text="Enter the name of this category.")
	description = models.TextField(blank=True, help_text="Enter an optional description for this category.")
	topics = models.ManyToManyField(Topic, help_text="Select the topics that are included in this category.")
	
	class Meta:
		ordering = ['category']
		verbose_name_plural = 'Categories'
	
	def __unicode__(self):
		return u'%s' % self.category

class Article(search.Model, models.Model):
	
	all_objects = models.Manager()
	objects = models.Manager()
	all_objects = models.Manager()
	item_url = 'healthday/article'
	search_order = 9
	ajax_search_limit = 5
	search_limit = 10
	
	for_update = models.PositiveSmallIntegerField(default=0, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Uncheck this box to remove this article from display and search on the site.", editable=False)
	article_id = models.CharField(primary_key=True, max_length=20, editable=False)
	urlname = models.CharField(max_length=50, editable=False, unique=True)
	posting_time = models.DateTimeField(blank=True, editable=False)
	archive_date = models.DateField(blank=True, editable=False)
	news_type = models.CharField(max_length=30, blank=True, editable=False)
	headline = models.CharField(max_length=200)
	blurb = models.CharField(max_length=1000, blank=True, editable=False)
	byline = models.CharField(max_length=100, blank=True)
	body = models.TextField()
	feature_blurb = models.CharField(max_length=1000, blank=True, editable=False)
	feature_image = models.CharField(max_length=500, blank=True, editable=False)
	attribution = models.CharField(max_length=100, blank=True, editable=False)
	tagline = models.CharField(max_length=100, blank=True, editable=False)
	source = models.CharField(max_length=1000, blank=True, editable=False)
	copyright = models.CharField(max_length=500, blank=True, editable=False)
	topics = models.ManyToManyField(Topic)
	
	class Meta:
		ordering = ['posting_time']
		verbose_name = "Health In The News Article"
		verbose_name_plural = "Health In The News Articles"
	
	def content(self):
		return self.body
	
	def __unicode__(self):
		return u'%s' % (self.headline)
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def meta_description(self):
		return self.blurb
	
	def display_time(self):
		return u'%s' % self.posting_time.strftime('%B %d, %Y')
	
	def relative_age(self):
		# For index pages -- within the last week, or month, or year
		if self.posting_time >= datetime.today() - timedelta(days=7):
			return 'Within the last week'
		if self.posting_time >= datetime.today() - timedelta(days=30):
			return 'Within the last month'
		if self.posting_time >= datetime.today() - timedelta(days=365):
			return 'Within the last year'
		return 'Older than one year'
	
	def search_index(self):
		if self.posting_time >= datetime(2009, 1, 1):
			# Return a (key, url, order, display, name, body) tuple with text for indexing
			return SearchKey(self.article_id, self.get_absolute_url(), self.posting_time.isoformat(), self.headline, self.headline, self.body)
		return None

	def display_image(self):
		if self.feature_image:
			return self.feature_image
		else:
			return None
