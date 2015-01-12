import hashlib
from datetime import datetime, timedelta
import time
import re

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static

from smgsite.settings import MEDIA_URL
from smgsite.services.models import Service
import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.marketing_banners.models import MarketingBanner
from smgsite.search.containers import SearchKey
from smgsite.site import image_make_thumbnail
from smgsite.doctors.models import Doctor

IMAGE_MAX_WIDTH = 240
IMAGE_MAX_HEIGHT = 240
THUMB_MAX_WIDTH = 50
THUMB_MAX_HEIGHT = 50

ARCHIVE_AGE = 365 # Days before this is described as an "archive" article

def common_relative_age(model):
	# For index pages -- within the last week, or month, or year
	#if model.posting_time >= datetime.today() - timedelta(days=7):
	#	return 'Within the last week'
	if model.posting_time >= datetime.today() - timedelta(days=30):
		return 'Within the Last Month'
	if model.posting_time >= datetime.today() - timedelta(days=365):
		return 'Within the Last Year'
	return 'Older Than One Year'


class MissingImage(object):

    def __init__(self, name):
        self.name = name


class URLAlias(cms.Model, models.Model):
	"""
	Model for URL Aliases
	"""
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this URL alias.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for this alias URL (e.g. 'breaking-news')")

	class Meta:
		ordering = ['urlname']
		verbose_name = "URL Alias"
		verbose_name_plural = "URL Aliases"
	
	def __unicode__(self):
		return u'%s' % self.urlname


class Manager(models.Manager):
	def get_query_set(self):
		return super(Manager, self).get_query_set().filter(active=u'1', for_update__lte=1, posting_time__lte=datetime.now())


class Article(cms.Model, search.Model, models.Model):
	
	qa_objects = cms.QAManager()
	objects = Manager()
	all_objects = models.Manager()
	item_url = 'article'
	search_order = 8
	search_limit = 10
	
	PROMO = (
		(0, 'Off'),
		(1, 'Position 1'),
		(2, 'Position 2'),
		(3, 'Position 3'),
		(4, 'Position 4'),
		(5, 'Position 5'),
		(6, 'Position 6'),
	)
	
	content_default = '<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'	
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this article from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Health-At-SMG' to have this Event load at '/article/Health-At-SMG/'). This is normally created for you from the headline.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this article will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the article is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the article display, and can be changed to reflect updates.")
	headline = models.CharField(max_length=200, help_text="Enter the headline of this article.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this article.")
	byline_link = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline link for this article. This can be relative, like '/services/' or fully qualified, like 'http://www.sumitmedicalgroup.com'. Be sure to test.")
	content = models.TextField(default=content_default, help_text="Enter the article body and more information line above. To create the link, 1) replace the placeholder with the display text for the link, e.g. American Academy of Pediacrics; 2) select the display text so that it is highlighted; 3) choose the link button from the toolbar to insert the link.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/article-images', help_text="Upload an image for this article. For homepage leaders, this image will be used as the preview and next/previous button image. This image will automatically be scaled.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/article-images')
	service = models.ForeignKey(Service, blank=True, null=True, help_text="Enter service page for this artice (e.g. select Cardiolgy to have this article only display on the Cardiology service page). Do not select a service if this article should appear on the home page.")
	leader_promo = models.PositiveSmallIntegerField(default=0, choices=PROMO, help_text="Select Off for normal articles, or select the position for rotation of this article on the homepage leader.")
	headline_promo = models.PositiveSmallIntegerField(default=0, choices=PROMO, help_text="Select Off for normal articles, or select the position for this headline under \"Our News\" on the home page.")
	reviewed_by = models.CharField(max_length=100, blank=True, help_text="Optionally enter a reviewed by notation.")
	reviewed_by_link = models.CharField(max_length=200, blank=True, help_text="Optionally enter a a link for the reviewed by notation")
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="articles_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	blurb = models.TextField(
		blank=True,
		help_text='Blurb text should be a short summary of the article, it will display on preview lists' )
	class Meta:
		ordering = ['-posting_time']
		verbose_name = "SMG Article"
		verbose_name_plural = "SMG Articles"
	
	def __unicode__(self):
		return u'%s' % (self.headline)
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')
	
	def relative_age(self):
		return common_relative_age(self)

	@staticmethod	
	def is_live(key):
		try:
			posting_time = Article.all_objects.get(id=key).posting_time
			return posting_time <= datetime.now()
		except:
			return False
	
	def is_archive(self):
		return self.posting_time < datetime.today() - timedelta(days=ARCHIVE_AGE)
	
	def clearcache(self):
		for i in range(len(self.PROMO)):
			path = reverse('smgsite.articles.views.leader', kwargs={'position': i + 1})
			key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
			args = hashlib.md5(path)
			path = args.hexdigest()
			header_key = 'views.decorators.cache.cache_header.%s.%s' % (key_prefix, path)
			headers = cache.get(header_key)
			ctx = hashlib.md5()
			if headers:
				for header in headers:
					ctx.update(header)

			cache.delete(header_key)

			page_key = 'views.decorators.cache.cache_page.%s.%s.%s' % (key_prefix, path, ctx.hexdigest())
			cache.delete(page_key)

	def save(self, preview=True, post=True):
		super(Article, self).save(preview=preview, post=post)
		self.clearcache()
	
	def delete(self, preview=True):
		from django import forms
		if self.leader_promo == 0:
			leaders = Article.objects.filter(leader_promo__gt=0)
			if len(leaders) <= 1:
				raise forms.ValidationError('This is the last Homepage Leader news story. It cannot be deleted or reset as a non-leader story until there is another Leader news story. There must always be at least one Leader for the Homepage.')
		super(Article, self).delete(preview)
		self.clearcache()
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		if self.posting_time.__class__ == unicode:
			posting_time = datetime(*time.strptime(self.posting_time, "%Y-%m-%d %H:%M:%S")[0:5])
		else:
			posting_time = self.posting_time
		body = "%s %s" % (self.headline, self.content)
		return SearchKey(self.pk, self.get_absolute_url(), posting_time.isoformat(), self.headline, self.headline, body)


	def display_image(self):
		if self.original_image:
			return self.original_image
		else:
			return None
	@property
	def image(self):
		if self.original_image:
			return self.original_image
		else:
			return None


"""
Features are content-specific types of artices,
with independent listings and displays,
launcing with Nutrition and Fitness models.
"""

class Feature(cms.Model, search.Model, models.Model):
	
	qa_objects = cms.QAManager()
	objects = Manager()
	all_objects = models.Manager()
	item_url = 'feature'
	search_order = 7
	search_limit = 10
	
	FEATURES = (
		('F', 'Fitness'),
		('N', 'Nutrition'),
	)

	content_default = '<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'	
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this feature from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Health-At-SMG' to have this Event load at '/feature/Health-At-SMG/'). This is normally created for you from the headline.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	content_type = models.CharField(max_length=1, blank=False, null=False, choices=FEATURES)
	posting_time = models.DateTimeField(help_text="Set the posting time to when this feature will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the feature is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the feature display, and can be changed to reflect updates.")
	headline = models.CharField(max_length=200, help_text="Enter the headline of this feature.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this feature.")
	byline_link = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline link for this article. This can be relative, like '/services/' or fully qualified, like 'http://www.sumitmedicalgroup.com'. Be sure to test.")
	content = models.TextField(default=content_default, help_text="Enter the feature body and more information line above. To create the link, 1) replace the placeholder with the display text for the link, e.g. American Academy of Pediacrics; 2) select the display text so that it is highlighted; 3) choose the link button from the toolbar to insert the link.")
	related_recipes = models.ManyToManyField('Recipe', blank=True, null=True, related_name='recipes_related', help_text="Select optional related recipes for this feature.")
	reviewed_by = models.CharField(max_length=100, blank=True, help_text="Optionally enter a reviewed by notation.")
	reviewed_by_link = models.CharField(max_length=200, blank=True, help_text="Optionally enter a a link for the reviewed by notation")
	
	class Meta:
		ordering = ['-posting_time']
		verbose_name = "SMG Feature"
		verbose_name_plural = "SMG Features"
	
	def __unicode__(self):
		return u'%s' % (self.headline)
	
	def get_absolute_url(self):
		return "/%s/%s/%s/" % (self.item_url, self.get_content_type_display(), self.urlname)
	
	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')
	
	def relative_age(self):
		return common_relative_age(self)

	@staticmethod	
	def is_live(key):
		try:
			posting_time = Feature.all_objects.get(id=key).posting_time
			return posting_time <= datetime.now()
		except:
			return False
	
	def is_archive(self):
		return self.posting_time < datetime.today() - timedelta(days=ARCHIVE_AGE)
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		if self.posting_time.__class__ == unicode:
			posting_time = datetime(*time.strptime(self.posting_time, "%Y-%m-%d %H:%M:%S")[0:5])
		else:
			posting_time = self.posting_time
		body = "%s %s" % (self.headline, self.content)
		return SearchKey(self.pk, self.get_absolute_url(), posting_time.isoformat(), self.headline, self.headline, body)


class PressRelease(cms.Model, models.Model):

	qa_objects = cms.QAManager()
	objects = Manager()
	all_objects = models.Manager()
	item_url = 'press-release'
	search_order = 8
	search_limit = 10
	
	content_default = '<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'	
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this press release from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Health-At-SMG' to have this Event load at '/press-release/Health-At-SMG/'). This is normally created for you from the headline.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	headline = models.CharField(max_length=200, help_text="Enter the headline of this press release.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this press release.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this press release will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the press release is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the press release display, and can be changed to reflect updates.")
	content = models.TextField(default=content_default, help_text="Enter the press release body and more information line above. To create the link, 1) replace the placeholder with the display text for the link, e.g. American Academy of Pediacrics; 2) select the display text so that it is highlighted; 3) choose the link button from the toolbar to insert the link.")
	use_boilerplate = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Active to have the boilerplate intro and links HTML be displayed with this press release.")
	
	class Meta:
		ordering = ['-posting_time']
		verbose_name = "Press Release"
		verbose_name_plural = "Press Releases"

	def __unicode__(self):
		return u'%s' % (self.headline)
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')
	
	def relative_age(self):
		return common_relative_age(self)

	@staticmethod	
	def is_live(key):
		try:
			posting_time = PressRelease.all_objects.get(id=key).posting_time
			return posting_time <= datetime.now()
		except:
			return False

	def is_archive(self):
		return self.posting_time < datetime.today() - timedelta(days=ARCHIVE_AGE)
	

"""
Recipes are closely related to features,
but have enough custom fields to warrant
a separate model.
"""

class Recipe(cms.Model, search.Model, models.Model):

	qa_objects = cms.QAManager()
	objects = Manager()
	all_objects = models.Manager()
	item_url = 'recipe'
	search_order = 7
	search_limit = 10

	TYPES = (
		('B', 'Breakfast'),
		('L', 'Lunch'),
		('D', 'Dinner'),
		('S', 'Snack'),
		('E', 'Entertaining'),
		('B', 'Beverage'),
		('K', 'Kids'),
	)

	FEATURED = (
			(u'1', 'Featured'),
			(u'0', 'Not Featured'),
	)

	content_default = '<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this feature from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Health-At-SMG' to have this Event load at '/feature/Health-At-SMG/'). This is normally created for you from the title.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this feature will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the feature is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the feature display, and can be changed to reflect updates.")
	title = models.CharField(max_length=200, help_text="Enter the title of this feature.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this feature.")
	byline_link = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline link for this article. This can be relative, like '/services/' or fully qualified, like 'http://www.sumitmedicalgroup.com'. Be sure to test.")
	recipe_type = models.CharField(max_length=1, blank=False, null=False, choices=TYPES)
	featured = models.CharField(max_length=1, default=u'0', choices=FEATURED, help_text="Select Featured to chose this as the featured recipe. Only one recipe can be featured at a time.")
	original_image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/recipe-images', help_text="Upload an image for this recipe. This image will automatically be scaled.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/recipe-images')
	description = models.TextField(default='Description', blank=True, help_text="Enter the description of this recipe.")
	ingredients = models.TextField(default='Ingredients', help_text="Enter the ingredients for this recipe, one per line.")
	directions = models.TextField(default='Directions', help_text="Enter the directions for this recipe, one step per line.")
	notes = models.TextField(default='Notes', blank=True, help_text="Enter any additional notes for this recipe.")
	reviewed_by = models.CharField(max_length=100, blank=True, help_text="Optionally enter a reviewed by notation.")
	reviewed_by_link = models.CharField(max_length=200, blank=True, help_text="Optionally enter a a link for the reviewed by notation")


	serving_size = models.CharField(max_length=10, blank=True, help_text="Serving size")
	num_servings = models.CharField(max_length=5, blank=True, help_text="Number of servings")
	calories = models.CharField(max_length=5, blank=True, help_text="Calories")
	fat_cals = models.CharField(max_length=5, blank=True, help_text="Calories from fat")
	total_fat = models.CharField(max_length=5, blank=True, help_text="Grams Total fat")
	saturated_fat = models.CharField(max_length=5, blank=True, help_text="Grams Saturated fat")
	trans_fat = models.CharField(max_length=5, blank=True, help_text="Grams Trans fat")
	cholesterol = models.CharField(max_length=5, blank=True, help_text="mg Cholesterol")
	sodium = models.CharField(max_length=5, blank=True, help_text="mg Sodium")
	total_carbs = models.CharField(max_length=5, blank=True, help_text="Grams Total Carbohydrates")
	dietary_fiber = models.CharField(max_length=5, blank=True, help_text="Grams Dietary Fiber")
	sugars = models.CharField(max_length=5, blank=True, help_text="Grams Sugars")
	protein = models.CharField(max_length=5, blank=True, help_text="Grams Protein")
	vit_a = models.CharField(max_length=5, blank=True, help_text="% Vitamin A")
	vit_c = models.CharField(max_length=5, blank=True, help_text="% Vitamin C")
	calcium = models.CharField(max_length=5, blank=True, help_text="% Calcium")
	iron = models.CharField(max_length=5, blank=True, help_text="% Iron")

	class Meta:
		ordering = ['-posting_time']
		verbose_name = "SMG Recipe"
		verbose_name_plural = "SMG Recipes"

	def __unicode__(self):
		return u'%s' % (self.title)

	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)

	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')

	def relative_age(self):
		return common_relative_age(self)

	def ingredient_list(self):
		return self.ingredients.split('\n')

	def direction_list(self):
		return self.directions.split('\n')

	def pct_total_fat(self):
		if not self.total_fat:
			return None
		return '%d%%' % (float(self.total_fat) / 65 * 100)

	def pct_saturated_fat(self):
		if not self.saturated_fat:
			return None
		return '%d%%' % (float(self.saturated_fat) / 20 * 100)

	def pct_cholesterol(self):
		if not self.cholesterol:
			return None
		return '%d%%' % (float(self.cholesterol) / 300 * 100)

	def pct_sodium(self):
		if not self.sodium:
			return None
		return '%d%%' % (float(self.sodium) / 2300 * 100)

	def pct_total_carbs(self):
		if not self.total_carbs:
			return None
		return '%d%%' % (float(self.total_carbs) / 300 * 100)

	def pct_dietary_fiber(self):
		if not self.dietary_fiber:
			return None
		return '%d%%' % (float(self.dietary_fiber) / 25 * 100)

	def pct_protein(self):
		if not self.protein:
			return None
		return '%d%%' % (float(self.protein) / 50 * 100)

	def save(self, preview=True):
		if self.original_image:
			image_make_thumbnail(self, 'original_image', 'image', 'db/recipe-images', IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT)
		super(Recipe, self).save(preview)

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		if self.posting_time.__class__ == unicode:
			posting_time = datetime(*time.strptime(self.posting_time, "%Y-%m-%d %H:%M:%S")[0:5])
		else:
			posting_time = self.posting_time
		body = "%s %s %s" % (self.title, self.description, self.ingredients)
		return SearchKey(self.pk, self.get_absolute_url(), posting_time.isoformat(), self.title, self.title, body)

"""
PDFs are used for links to PDF documents.
"""

class PDF(cms.Model, models.Model):

	qa_objects = cms.QAManager()
	objects = Manager()
	all_objects = models.Manager()
	item_url = 'pdf'
	search_order = 6
	search_limit = 10

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this pdf from display and search on the site.")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this pdf will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the pdf is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the pdf display, and can be changed to reflect updates.")
	title = models.CharField(max_length=200, help_text="Enter the title of this pdf.")
	description = models.TextField(blank=True, help_text="Enter an optional description for this PDF.")
	pdf = models.FileField(blank=True, null=True, upload_to='db/pdf-files', help_text="Upload the PDF.")
	thumbnail = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/pdf-files', help_text="Upload an image thumbnail for this recipe.")

	class Meta:
		ordering = ['-posting_time']
		verbose_name = "SMG PDF"
		verbose_name_plural = "SMG PDFs"

	def __unicode__(self):
		return u'%s' % (self.title)

	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')

	def relative_age(self):
		return common_relative_age(self)

	@staticmethod
	def is_live(key):
		try:
			posting_time = Feature.all_objects.get(id=key).posting_time
			return posting_time <= datetime.now()
		except:
			return False

	def is_archive(self):
		return self.posting_time < datetime.today() - timedelta(days=ARCHIVE_AGE)

"""
Media Results and Trending Topics
"""

class MediaResult(cms.Model, search.Model, models.Model):

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'recentcoverage'
	search_order = 8
	search_limit = 10

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this media result from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter folder for URL (e.g. enter 'Health-At-SMG' to have this media result load at '/recentcoverage/Health-At-SMG/'). This is normally created for you from the headline.")
	aliases = models.ManyToManyField(URLAlias, blank=True, null=True, help_text="URL Aliases")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this feature will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the feature is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the feature display, and can be changed to reflect updates.")
	headline = models.CharField(max_length=200, help_text="Enter the headline of this feature.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this Media Result.")
	byline_link = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline link for this Media Result. This can be relative, like '/services/' or fully qualified, like 'http://www.sumitmedicalgroup.com'. Be sure to test.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/mediaresult-images', help_text="Upload an image for this media result.")
	content = models.TextField(help_text="Enter the media result body above.")
	marketing_banner = models.ForeignKey(MarketingBanner, related_name="mediaresult_marketing_banner", blank=True, null=True, help_text="Enter an additional marketing banner to be associated with this page.")
	sort_order = models.PositiveSmallIntegerField(default=None, null=True, help_text="Select the sort order position for this trending topic. Set to 0 to remove from ordering.")
	blurb = models.TextField(
		blank=True,
		help_text='Blurb text should be a short summary of the article, it will display on preview lists' )
	class Meta:
		ordering = ['-posting_time']
		verbose_name = "SMG Media Result"
		verbose_name_plural = "SMG Media Results"

	def __unicode__(self):
		return u'%s' % (self.headline)

	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)

	def display_time_for_display(self):
		return u'%s' % self.display_time.strftime('%m-%d-%Y')

	def relative_age(self):
		return common_relative_age(self)

	@staticmethod
	def is_live(key):
		try:
			posting_time = Feature.all_objects.get(id=key).posting_time
			return posting_time <= datetime.now()
		except:
			return False

	def is_archive(self):
		return self.posting_time < datetime.today() - timedelta(days=ARCHIVE_AGE)

	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		if self.posting_time.__class__ == unicode:
			posting_time = datetime(*time.strptime(self.posting_time, "%Y-%m-%d %H:%M:%S")[0:5])
		else:
			posting_time = self.posting_time
		body = "%s %s" % (self.headline, self.content)
		return SearchKey(self.pk, self.get_absolute_url(), posting_time.isoformat(), self.headline, self.headline, body)

	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		if self.posting_time.__class__ == unicode:
			posting_time = datetime(*time.strptime(self.posting_time, "%Y-%m-%d %H:%M:%S")[0:5])
		else:
			posting_time = self.posting_time
		return SearchKey(self.pk, self.get_absolute_url(), posting_time.isoformat(), self.headline, self.keywords, self.keywords)

	def save(self, preview=True, post=True):
		if self.sort_order == 0:
			self.sort_order = None
		super(MediaResult, self).save(preview=preview, post=post)


class TrendingTopic(cms.Model, models.Model):

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this media result from display and search on the site.")
	headline = models.CharField(max_length=200, help_text="Enter the headline of this trending topic.")
	content = models.TextField(help_text="Enter the content of this trending topic.")
	experts = models.ManyToManyField(Doctor, blank=True, help_text="Select the SMG professionals who are experts for this topic.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/trending-images', help_text="Upload an image for this trending topic.")
	sort_order = models.PositiveSmallIntegerField(default=None, null=True, help_text="Select the sort order position for this trending topic. Set to 0 to remove from ordering.")

	class Meta:
		ordering = ['-sort_order']
		verbose_name = "SMG Trending Topics"
		verbose_name_plural = "SMG Trending Topics"

	def __unicode__(self):
		return u'%s' % (self.headline)

	def save(self, preview=True, post=True):
		if self.sort_order == 0:
			self.sort_order = None
		super(TrendingTopic, self).save(preview=preview, post=post)

