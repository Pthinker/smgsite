from datetime import datetime, timedelta

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, InvalidPage

from smgsite.healthday.models import Article, Topic, Category
from smgsite.pages.models import Page
from smgsite.settings import RSS_COUNT
from smgsite.site.paginator import DiggPaginator
from django.core.paginator import InvalidPage, EmptyPage

ARTICLES_PER_PAGE = 50
ADDITIONAL_PAGES_LISTED = 6 # Pages on each side of the current page, must be an even number

def news_by_category(request, category_pk, template, url, page=1, contentpath=None):
	category = Category.objects.get(pk=category_pk)
	news_list = Article.objects.filter(topics__in=category.topics.all()).order_by('-posting_time').distinct()
	paginator = DiggPaginator(news_list, ARTICLES_PER_PAGE)
	
	# get service content
	try:
		page_obj = Page.objects.get(urlname=contentpath)
		content = page_obj.content
	except Page.DoesNotExist:
		content = ''

	try:
		news = paginator.page(page)
	except (EmptyPage, InvalidPage):
		news = paginator.page(paginator.num_pages)
	
	return render(request, template, {'page':news, 'url':url, 'content': content})


def landing(request):
	"""
	This renders the article landing page.
	"""
	webscout = Article.objects.filter(news_type='WebScout').order_by('-posting_time')[0]
	ws_last_updated = webscout.posting_time.strftime('%a, %b %d, %Y')
	stories = Article.objects.filter(news_type='News').order_by('-posting_time')[:5]
	st_last_updated = stories[0].posting_time.strftime('%a, %b %d, %Y')
	fda = Article.objects.filter(news_type='FDA Approvals').order_by('-posting_time')[:5]
	fyi = Article.objects.filter(news_type='FYI').order_by('-posting_time')[:5]
	categories = Category.objects.order_by('category')
	ctx = {
		'webscout': webscout, 
		'ws_last_updated': ws_last_updated, 
		'stories': stories, 
		'st_last_updated': st_last_updated, 
		'fda': fda, 
		'fyi': fyi, 
		'categories': categories,
		}
	return render_to_response('articles/healthday-landing.html', ctx, context_instance=RequestContext(request))

def index(request, news_type, page=1):
	"""
	This renders the article index page.
	"""
	topic = None
	if news_type == 'all':
		objects = Article.objects.order_by('-posting_time')
	elif news_type in ('Webscout', 'News', 'FDA Approvals'):
		objects = Article.objects.filter(news_type=news_type).order_by('-posting_time')
	else:
		try:
			topic = Topic.objects.get(topic_name=news_type)
		except Topic.DoesNotExist:
			raise Http404
		except Topic.MultipleObjectsReturned:
			for topic in Topic.objects.filter(topic_name=news_type):
				if len(topic.article_set.all()) > 0:
					break
		objects = Article.objects.filter(topics__topic_name=news_type).order_by('-posting_time')
	category = None
	if request.GET.get('category'):
		try:
			category = Category.objects.get(pk=request.GET['category'])
			objects = objects.filter(topics__in=category.topics.all()).distinct()
		except Category.DoesNotExist:
			objects = []

	fyi = Article.objects.filter(news_type='FYI').order_by('-posting_time')[:5]
	categories = Category.objects.order_by('category')

	paginator = DiggPaginator(objects, ARTICLES_PER_PAGE)
	try:
		articles = paginator.page(page)
	except (EmptyPage, InvalidPage):
		articles = paginator.page(paginator.num_pages)

	url = None
	if category:
		url = '/healthday/all/'
	if news_type:
		url = '/healthday/%s/' % news_type

	ctx = {
		'fyi': fyi, 
		'categories': categories, 
		'news_type': news_type, 
		'category': category, 
		'topic': topic,
		'url': url,
		'page': articles,
	}

	return render_to_response('articles/healthday-index.html', ctx , context_instance=RequestContext(request))

def rss(request):
	"""
	This renders the RSS feed for healthday news on the site.
	"""
	articles = Article.objects.order_by('-posting_time')[:RSS_COUNT]
	return render_to_response('rss/healthday.html', {'articles': articles}, context_instance=RequestContext(request))

def topic_rss(request, topic):
	"""
	This renders the RSS feed for healthday news on the site for a selected topic.
	"""
	topic = Topic.objects.get(pk=topic)
	articles = Article.objects.filter(topics__in=[topic]).order_by('-posting_time')[:RSS_COUNT]
	return render_to_response('rss/healthday.html', {'articles': articles, 'topic': topic}, context_instance=RequestContext(request))

def category_rss(request, category):
	"""
	This renders the RSS feed for healthday news on the site for a selected category.
	"""
	category = Category.objects.get(pk=category)
	articles = Article.objects.filter(topics__in=category.topics.all()).distinct().order_by('-posting_time')[:RSS_COUNT]
	return render_to_response('rss/healthday.html', {'articles': articles, 'category': category}, context_instance=RequestContext(request))

def type_rss(request, news_type):
	"""
	This renders the RSS feed for healthday news on the site for a selected news type.
	"""
	articles = Article.objects.filter(news_type=news_type).order_by('-posting_time')[:RSS_COUNT]
	return render_to_response('rss/healthday.html', {'articles': articles, 'news_type': news_type}, context_instance=RequestContext(request))

def article(request, urlname):
	"""
	This renders the article display page.
	"""
	try:
		article = Article.objects.get(urlname=urlname)
	except Article.DoesNotExist:
		raise Http404
	fyi = Article.objects.filter(news_type='FYI').order_by('-posting_time')[:5]
	topics = [x.topic_name for x in article.topics.all()]
	categories = Category.objects.order_by('category')
	return render_to_response('articles/healthday-article.html', {'article': article, 'topics': topics, 'fyi': fyi, 'categories': categories}, context_instance=RequestContext(request))


