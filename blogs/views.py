from datetime import datetime, timedelta
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Q
from smgsite.settings import CACHE_TIME
from django import forms
from django.forms import extras
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets as admin_widgets
from smgsite.blogs.models import Blog, BlogEntry, BlogSection, BlogEntrySection
from smgsite.healthday.models import Article
from smgsite.settings import RSS_COUNT

def index(request):
	"""
	View method to present a list of all the blogs on the site.
	"""
	if request.user.is_authenticated():
		blogs = Blog.qa_objects.order_by('name')
	else:
		blogs = Blog.objects.order_by('name')
	return render_to_response('blogs/blogs.html', {'blogs': blogs}, context_instance=RequestContext(request))


class SectionDisplay(object):
	def __init__(self, section, is_authenticated):
		self.section = section
		yearago = datetime.now() - timedelta(days=365)
		if is_authenticated:
			self.posts = BlogEntry.qa_objects.filter(blog=section.blog, blogentrysection__section=section).filter(Q(posting_time__gte=yearago) | Q(exclude_from_archiving=u'1')).filter(posting_time__lte=datetime.now()).order_by('-posting_time')
		else:
			self.posts = BlogEntry.objects.filter(blog=section.blog, blogentrysection__section=section).filter(Q(posting_time__gte=yearago) | Q(exclude_from_archiving=u'1')).filter(posting_time__lte=datetime.now()).order_by('-posting_time')


def listing(request, urlname):
	"""
	View method to present a list of all the entries for a given blog.
	"""
	yearago = datetime.now() - timedelta(days=365)
	if request.user.is_authenticated():
		blog = Blog.qa_objects.get(urlname=urlname)
		sections = BlogSection.qa_objects.filter(blog=blog).order_by('position')
	else:
		blog = Blog.objects.get(urlname=urlname)
		sections = BlogSection.objects.filter(blog=blog).order_by('position')
	display_sections = []
	for section in sections:
		if not section.blogentry_section.filter(Q(entry__posting_time__gte=yearago) | Q(entry__exclude_from_archiving=u'1') | Q(entry__posting_time__gt=datetime.now())):
			continue
		display_section = SectionDisplay(section, request.user.is_authenticated())
		display_sections.append(display_section)
	return render_to_response('blogs/blog.html', {'blog': blog, 'sections': display_sections}, context_instance=RequestContext(request))

def full_listing(request, urlname):
	"""
	View method to present a list of all the entries for a given blog.
	"""
	if request.user.is_authenticated():
		blog = Blog.qa_objects.get(urlname=urlname)
		posts = BlogEntry.qa_objects.filter(blog=blog, posting_time__lte=datetime.now()).order_by('-posting_time')
	else:
		blog = Blog.objects.get(urlname=urlname)
		posts = BlogEntry.objects.filter(blog=blog).order_by('-posting_time')
	return render_to_response('blogs/full.html', {'blog': blog, 'posts': posts}, context_instance=RequestContext(request))

def post(request, blog, urlname):
	"""
	View method to display a single post.
	"""
	if request.user.is_authenticated():
		blog = Blog.qa_objects.get(urlname=blog)
		post = BlogEntry.qa_objects.get(blog=blog, urlname=urlname)
		posts = BlogEntry.qa_objects.filter(blog=blog).order_by('-posting_time')[:5]
		blogs = Blog.qa_objects.order_by('name')
	else:
		blog = Blog.objects.get(urlname=blog)
		post = BlogEntry.objects.get(blog=blog, urlname=urlname)
		posts = BlogEntry.objects.filter(blog=blog).order_by('-posting_time')[:5]
		blogs = Blog.objects.order_by('name')
	fyi = Article.objects.filter(news_type='FYI').order_by('-posting_time')[:5]	
	return render_to_response('blogs/post.html', {'blog': blog, 'post': post, 'posts': posts, 'fyi': fyi, 'blogs': blogs}, context_instance=RequestContext(request))

@login_required
def admin(request):
	"""
	View method where blog authors and editors can see an overview of all their blogs.
	"""
	blogs = Blog.objects.filter(authors=request.user)
	return render_to_response('blogs/admin/admin.html', {'user': request.user, 'blogs': blogs}, context_instance=RequestContext(request))

@login_required
def blogAdmin(request, urlname):
	"""
	View method where blog authors and editors can administer a specific blog.
	"""
	blog = Blog.objects.get(authors=request.user, urlname=urlname)
	editor = request.user in blog.editors.all()
	posts = BlogEntry.qa_objects.filter(blog=blog).order_by('-posting_time')
	return render_to_response('blogs/admin/blog_admin.html', {'user': request.user, 'editor': editor, 'blog': blog, 'posts': posts}, context_instance=RequestContext(request))

"""
Blog entry posting and editing methods
"""

class BlogForm(forms.Form):
	posting_time = forms.DateTimeField(widget=admin_widgets.AdminSplitDateTime())
	display_time = forms.DateTimeField(widget=admin_widgets.AdminSplitDateTime())
	keywords = forms.CharField(max_length=500, required=False)
	title = forms.CharField(max_length=100)
	byline = forms.CharField(max_length=100, required=False)
	byline_link = forms.CharField(max_length=100, required=False)
	reviewed_by = forms.CharField(max_length=100, required=False)
	reviewed_by_link = forms.CharField(max_length=100, required=False)
	body = forms.CharField(widget=forms.Textarea)
	sections = forms.MultipleChoiceField(widget=forms.SelectMultiple())
	urlname = forms.CharField(required=False, widget=forms.HiddenInput)

	def __init__(self, *args, **kwargs):
		if 'sections' in kwargs:
			sections = kwargs['sections']
			kwargs.pop('sections')
		else:
			sections = None
		if 'initial_sections' in kwargs:
			initial_sections = kwargs['initial_sections']
			kwargs.pop('initial_sections')
		else:
			initial_sections = None
		super(BlogForm, self).__init__(*args, **kwargs)
		if sections:
			self.fields['sections'].choices = sections
		if initial_sections:
			self.fields['sections'].initial = initial_sections
		self.fields['posting_time'].initial = datetime.now()
		self.fields['display_time'].initial = datetime.now()

@login_required
def blogEdit(request, urlname):
	"""
	View method for posting and editing blog entries.
	"""
	blog = Blog.objects.get(authors=request.user, urlname=urlname)
	sections = [(s.pk, s.name) for s in blog.blogsection_set.all()]
	editor = request.user in blog.editors.all()
	if request.method == 'POST':
		form = BlogForm(request.POST, sections=sections)
		if form.is_valid():
			data = form.cleaned_data
			if data['urlname']:
				post = BlogEntry.qa_objects.get(blog=blog, urlname=data['urlname'])
				post.title = data['title']
				post.byline = data['byline']
				post.byline_link = data['byline_link']
				post.reviewed_by = data['reviewed_by']
				post.reviewed_by_link = data['reviewed_by_link']
				post.body = data['body']
				for section in data['sections']:
					section_model = BlogSection.objects.get(pk=section)
					existing = BlogEntrySection.qa_objects.filter(entry=post, section=section_model)
					if not existing:
						new = BlogEntrySection(entry=post, section=section_model)
						post.blogentrysection_set.add(new)
			else:
				post = BlogEntry(for_update=2, blog=blog, urlname=None, author=request.user, title=data['title'], posting_time=data['posting_time'], display_time=data['display_time'], byline=data['byline'], byline_link=data['byline_link'], reviewed_by=data['reviewed_by'], reviewed_by_link=data['reviewed_by_link'], body=data['body'])
			post.save()
			return render_to_response('blogs/admin/blog_admin.html', {'user': request.user, 'editor': editor, 'blog': blog}, context_instance=RequestContext(request))
		else:
			return render_to_response('blogs/admin/blog_edit.html', {'form': form, 'user': request.user, 'editor': editor, 'blog': blog}, context_instance=RequestContext(request))
	else:
		if request.GET.get('entry'):
			entry = request.GET['entry']
			post = BlogEntry.qa_objects.get(blog=blog, urlname=entry)
			initial_sections = [s.pk for s in post.blogentrysection_set.all()]
			form = BlogForm(sections=sections, initial={'posting_time': post.posting_time, 'display_time': post.display_time, 'urlname': entry, 'title': post.title, 'byline': post.byline, 'byline_link': post.byline_link, 'reviewed_by': post.reviewed_by, 'reviewed_by_link': post.reviewed_by_link, 'body': post.body, 'sections': initial_sections})
		else:
			form = BlogForm(sections=sections)
		return render_to_response('blogs/admin/blog_edit.html', {'form': form, 'user': request.user, 'editor': editor, 'blog': blog}, context_instance=RequestContext(request))

def rss(request, blog):
	"""
	This renders the RSS feed for a blog.
	"""
	blog = Blog.objects.get(urlname=blog)
	articles = BlogEntry.objects.filter(blog=blog).order_by('-posting_time')[:RSS_COUNT]
	return render_to_response('rss/blog.html', {'blog': blog, 'articles': articles}, context_instance=RequestContext(request))
