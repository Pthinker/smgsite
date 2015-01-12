from django.db import models
from django.contrib.auth.models import User
import smgsite.cms.models as cms
import smgsite.search.models as search
from smgsite.search.containers import SearchKey


class Blog(cms.Model, search.Model, models.Model):
	"""
	Model for a blog
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'blog'
	search_order = 7
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this blog from display and search on the site.")
	urlname = models.CharField(max_length=50, unique=True, help_text="Enter identifier for URL (e.g. enter 'health' to have this blog load at '/blog/health/')")
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	meta_description = models.TextField(blank=True, help_text="Enter an optional meta description for SEO.")
	name = models.CharField(max_length=100, unique=True, help_text="Enter a name for this blog.")
	description = models.TextField(blank=True)
	authors = models.ManyToManyField(User, related_name='authors', help_text="Select one or more users who can write entries and edit their own entries on this blog.")
	editors = models.ManyToManyField(User, related_name='editors', help_text="Select one or more users who can write entries, edit entries, and publish entries and updates on this blog.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/blog-images', help_text="Upload an image for this blog. Please ensure the image is correctly scaled before uploading.")
	blurb = models.TextField(max_length=250, blank=True, help_text="Enter a blurb for this blog.")
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return u'%s' % self.name
	
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.urlname)
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s" % (self.name, self.description)
		return SearchKey(self.pk, self.get_absolute_url(), self.name, self.name, self.name, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.name, self.name, self.keywords, self.keywords)
	
	def count(self):
		return len(self.blogentry_set.filter(active=u'1', for_update__lte=1))
	
	def latest(self):
		try:
			return self.blogentry_set.filter(active=u'1', for_update__lte=1).order_by('postdate')[0]
		except IndexError:
			return None


class BlogEntry(cms.Model, search.Model, models.Model):
	"""
	Model for blog entries
	"""
	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'blog'
	search_order = 7
	search_limit = 10
	
	blog = models.ForeignKey(Blog)
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this blog entry from display and search on the site.")
	urlname = models.CharField(max_length=50, blank=True)
	keywords = models.CharField(max_length=500, blank=True, help_text="Enter optional Top Match keywords separated by spaces.")
	author = models.ForeignKey(User, help_text="Enter the author of this blog entry.")
	posting_time = models.DateTimeField(help_text="Set the posting time to when this blog post will appear live on the site. This date and time will also be used for sort order in lists. This should not be changed after the article is created.")
	display_time = models.DateTimeField(help_text="The display time is used for the blog entry display, and can be changed to reflect updates.")
	postdate = models.DateTimeField(auto_now_add=True)
	moddate = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=100, help_text="Enter a title for this blog entry.")
	byline = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline for this blog.")
	byline_link = models.CharField(max_length=100, blank=True, help_text="Optionally enter a byline link for this blog. This can be relative, like '/services/' or fully qualified, like 'http://www.sumitmedicalgroup.com'. Be sure to test.")
	reviewed_by = models.CharField(max_length=100, blank=True, help_text="Optionally enter a reviewed by notation.")
	reviewed_by_link = models.CharField(max_length=200, blank=True, help_text="Optionally enter a a link for the reviewed by notation")
	body = models.TextField(blank=True)
	exclude_from_archiving = models.CharField(max_length=1, default=u'0', choices=cms.Model.EXCLUDE, help_text="Select Exclude to prevent this post from being archived.")
	
	class Meta:
		ordering = ['-postdate']
		verbose_name = "Live Well News"
		verbose_name_plural = "Live Well News"
		unique_together = (('blog', 'urlname'), ('blog', 'title'))
	
	def __unicode__(self):
		return u'%s: %s' % (self.blog.name, self.title)

	def section_list(self):
		lstr = ''
		count = 0
		for entrysection in self.blogentrysection_set.all():
			if count > 0:
				lstr += '; '
			count += 1
			lstr += entrysection.section.name
		return lstr

	def save(self, preview=True):
		from datetime import datetime
		if not self.urlname:
			now = str(datetime.now().date())
			count = 0
			urlname = now
			while True:
				try:
					b = BlogEntry.all_objects.get(blog=self.blog, urlname=urlname)
					count += 1
					urlname = '%s-%s' % (now, count)
				except BlogEntry.DoesNotExist:
					break
			self.urlname = urlname
		super(BlogEntry, self).save(preview)
	
	def get_absolute_url(self):
		return "/%s/%s/%s" % (self.item_url, self.blog.urlname, self.urlname)
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		body = "%s %s" % (self.title, self.body)
		return SearchKey(self.pk, self.get_absolute_url(), self.title, self.title, self.title, body)
	
	def keyword_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for keyword indexing
		return SearchKey(self.pk, self.get_absolute_url(), self.title, self.title, self.keywords, self.keywords)


class BlogSection(cms.Model, models.Model):
	"""
	Model for Blog sections
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()

	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, help_text="Select Inactive to remove this item from display and search on the site.")
	blog = models.ForeignKey(Blog)
	name = models.CharField(max_length=100, unique=True, help_text="Enter a name for this section.")
	image = models.ImageField(blank=True, null=True, width_field='', height_field='', upload_to='db/blog-images', help_text="Upload an image for this section. Please ensure the image is correctly scaled before uploading.")
	blurb = models.TextField(blank=True)
	position = models.PositiveSmallIntegerField(default=1, help_text="Enter a number to set the order for this section. Smaller numbers appear first.")

	def __unicode__(self):
		return u"%s" % (self.name,)


class BlogEntrySection(models.Model):
	"""
	Model for the sections a BlogEntry belongs to
	"""

	entry = models.ForeignKey(BlogEntry)
	section = models.ForeignKey(BlogSection, related_name="blogentry_section")

	def __unicode__(self):
		return u"%s: %s" % (self.entry.title, self.section.name)

