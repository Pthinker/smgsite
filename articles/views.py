from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from smgsite.settings import CACHE_TIME
from smgsite.articles.models import Article, PressRelease, Feature, Recipe, PDF, MediaResult, TrendingTopic

from smgsite.site.paginator import DiggPaginator

ARTICLES_PER_PAGE = 50
PRESS_RELEASES_PER_PAGE = 50
ADDITIONAL_PAGES_LISTED = 6 # Pages on each side of the current page, must be an even number

def index(request, page=1):
	"""
	This renders the article index page.
	"""
	if request.user.is_authenticated():
		articles = Article.qa_objects.exclude(leader_promo__gt=0).order_by('-posting_time')
	else:
		articles = Article.objects.exclude(leader_promo__gt=0).order_by('-posting_time')

	paginator = DiggPaginator(articles, ARTICLES_PER_PAGE)

	try:
		paged_articles = paginator.page(page)
	except (EmptyPage, InvalidPage):
		paged_articles = paginator.page(paginator.num_pages)

	ctx = {
		'page': paged_articles,
		'url': '/articles/',
	}

	return render(request, 'articles/articles.html', ctx)

@cache_page(CACHE_TIME)
def leader(request, position):
	if request.user.is_authenticated():
		leaders = Article.qa_objects.filter(leader_promo__gt=0).order_by('leader_promo')
	else:
		leaders = Article.objects.filter(leader_promo__gt=0).order_by('leader_promo')
	leader = leaders[(int(position)) % len(leaders)]
	return render_to_response('helpers/leader.html', {'leader': leader}, context_instance=RequestContext(request))

def article(request, urlname):
	"""
	This renders the article display page.
	"""
	try:
		if request.user.is_authenticated():
			article = Article.qa_objects.get(urlname=urlname)
		else:
			article = Article.objects.get(urlname=urlname)
	except Article.DoesNotExist:
		raise Http404
	return render_to_response('articles/article.html', {'article': article}, context_instance=RequestContext(request))

@login_required
def admin_article_reorder(request):
	articles = Article.objects.all().order_by('-posting_time')
	return render_to_response('admin/articles/article/reorder.html', {'error': None, 'articles': articles, 'leader_options': Article.PROMO, 'headline_options': Article.PROMO}, context_instance=RequestContext(request))

@login_required
def admin_set_article_reorder(request):
	error = False
	if request.method == 'POST':
		# First confirm that there are no duplicates, and at least one headline
		leaders = dict()
		headlines = dict()
		l_changes = dict()
		h_changes = dict()
		for v in request.POST.iterlists():
			if v[0].startswith('leader_promo'):
				try:
					leaders[v[1][0]] += 1
					if v[1][0] != '0':
						error = True
				except KeyError:
					leaders[v[1][0]] = 1
				l_changes[int(v[0][v[0].rindex('_')+1:])] = int(v[1][0])
			if v[0].startswith('headline_promo'):
				try:
					headlines[v[1][0]] += 1
					if v[1][0] != '0':
						error = True
				except KeyError:
					headlines[v[1][0]] = 1
				h_changes[int(v[0][v[0].rindex('_')+1:])] = int(v[1][0])
		if len(leaders) == 0:
			error = True
		if len(headlines) == 0:
			error = True
		if not error:
			for a in Article.objects.all():
				change = False
				if l_changes.has_key(a.id) and a.leader_promo != l_changes[a.id]:
					change = True
					a.leader_promo = l_changes[a.id]
				if h_changes.has_key(a.id) and a.headline_promo != h_changes[a.id]:
					change = True
					a.headline_promo = h_changes[a.id]
				if change:
					a.save(preview=False, post=False)
			return HttpResponseRedirect('/admin/articles/article/')
	articles = Article.objects.all().order_by('-posting_time')
	return render_to_response('admin/articles/article/reorder.html', {'error': 'True', 'articles': articles, 'leader_options': Article.PROMO, 'headline_options': Article.PROMO}, context_instance=RequestContext(request))

def pr_index(request, year=0, page=1):
	"""
	This renders the press release index page.
	Only press releases for the current or select year are shown.
	A list of other years with available articles is also shown.
	"""
	print year
	if year == 0:
		year = unicode(date.today().year)
	if request.user.is_authenticated():
		years = [unicode(y.year) for y in PressRelease.objects.order_by('-posting_time').dates('posting_time', 'year') if y != None]
		paginator = Paginator(PressRelease.qa_objects.filter(posting_time__year=year).order_by('-posting_time'), ARTICLES_PER_PAGE)
	else:
		paginator = Paginator(PressRelease.objects.filter(posting_time__year=year).order_by('-posting_time'), ARTICLES_PER_PAGE)
		years = [unicode(y.year) for y in PressRelease.objects.order_by('-posting_time').dates('posting_time', 'year') if y != None]
	try:
		page = int(page)
	except ValueError:
		page = 1
	start = page - (ADDITIONAL_PAGES_LISTED / 2)
	if start < 0:
		start = 0
	pagelist = [x+1 for x in xrange(start, min(start+ADDITIONAL_PAGES_LISTED+1, paginator.num_pages))]
	pageobj = paginator.page(page)
	articles = pageobj.object_list
	previous = pageobj.has_previous()
	next = pageobj.has_next()
	showpages = False
	if paginator.num_pages > 1:
		showpages = True
	return render_to_response('articles/press-releases.html', {'articles': articles, 'showpages': showpages, 'page': page, 'pagelist': pagelist, 'previous': previous, 'next': next, 'year': year, 'years': years}, context_instance=RequestContext(request))

def press_release(request, urlname):
	"""
	This renders the press release display page.
	"""
	if request.user.is_authenticated():
		press_release = PressRelease.qa_objects.get(urlname=urlname)
	else:
		press_release = PressRelease.objects.get(urlname=urlname)
	return render_to_response('articles/press-release.html', {'press_release': press_release}, context_instance=RequestContext(request))


def features(request, content, page=1):
	"""
	This renders the features list page.
	"""
	try:
		key = [key for key,val in Feature.FEATURES if val==content][0]
	except IndexError:
		raise Http404

	if request.user.is_authenticated():
		feature_list = Feature.qa_objects.filter(content_type=key).order_by('-posting_time')
	else:
		feature_list = Feature.objects.filter(content_type=key).order_by('-posting_time')

	paginator = DiggPaginator(feature_list, ARTICLES_PER_PAGE)

	try:
		features = paginator.page(page)
	except (EmptyPage, InvalidPage):
		features = paginator.page(paginator.num_pages)

	ctx = {
		'page': features, 
		'content': content,
		'url': '/features/%s/' % content, 
	}

	template = 'articles/%s_list.html' % content.lower()
	return render(request, template, ctx)


def feature(request, content, urlname):
	"""
	This renders the feature details page.
	"""
	try:
		key = [key for key,val in Feature.FEATURES if val==content][0]
	except IndexError:
		raise Http404

	try:	
		if request.user.is_authenticated():
			feature = Feature.qa_objects.get(content_type=key, urlname=urlname)
		else:
			feature = Feature.objects.get(content_type=key, urlname=urlname)
	except Feature.DoesNotExist:
		raise Http404


	ctx = {
		'article': feature,
		'content': content,
	}
	template = 'articles/%s_detail.html' % content.lower()
	return render(request, template, ctx)


def recipes(request, page=1):
	"""
	This renders the recipe list page.
	"""
	if request.user.is_authenticated():
		recipe_list = Recipe.qa_objects.all().order_by('-posting_time')
	else:
		recipe_list = Recipe.objects.all().order_by('-posting_time')

	paginator = DiggPaginator(recipe_list, ARTICLES_PER_PAGE)

	try:
		recipes = paginator.page(page)
	except (EmptyPage, InvalidPage):
		recipes = paginator.page(paginator.num_pages)

	ctx = {
		'page': recipes,
	}

	template = 'articles/recipe_list.html'
	return render(request, template, ctx)


def recipe(request, urlname):
	"""
	This renders the recipe detail page.
	"""
	if request.user.is_authenticated():
		recipe = Recipe.qa_objects.get(urlname=urlname)
	else:
		recipe = Recipe.objects.get(urlname=urlname)
	template = 'articles/recipe_detail.html'
	return render(request, template, {'recipe': recipe})


def pdfs(request):
	"""
	This renders the PDF index page.
	"""
	if request.user.is_authenticated():
		top_pdfs = PDF.qa_objects.all().order_by('-posting_time')[0:4]
		next_pdfs = PDF.qa_objects.all().order_by('-posting_time')[4:]
	else:
		top_pdfs = PDF.objects.all().order_by('-posting_time')[0:4]
		next_pdfs = PDF.objects.all().order_by('-posting_time')[4:]
	template = 'articles/pdfs.html'
	return render_to_response(template, {'top_pdfs': top_pdfs, 'next_pdfs': next_pdfs}, context_instance=RequestContext(request))


@login_required
def admin_mediaresult_reorder(request):
	mediaresults = MediaResult.objects.all().order_by('-posting_time')
	return render_to_response('admin/articles/mediaresult/reorder.html', {'error': None, 'mediaresults': mediaresults, 'sort_options': ['None', 1, 2, 3, 4, 5]}, context_instance=RequestContext(request))


@login_required
def admin_set_mediaresult_reorder(request):
	error = False
	if request.method == 'POST':
		# First confirm that there are no duplicates
		for v in request.POST.iterlists():
			if v[0].startswith('mediaresult'):
				id = int(v[0][v[0].rindex('_')+1:])
				a = MediaResult.objects.get(id=id)
				if v[1][0] == 'None':
					a.sort_order = None
				else:
					a.sort_order = int(v[1][0])
				a.save(preview=False, post=False)
		return HttpResponseRedirect('/admin/articles/mediaresult/')
	mediaresults = MediaResult.objects.all().order_by('-posting_time')
	return render_to_response('admin/articles/mediaresult/reorder.html', {'error': None, 'mediaresults': mediaresults, 'sort_options': ['None', 1, 2, 3, 4, 5]}, context_instance=RequestContext(request))



# NEWSROOM VIEWS

def newsroom_index(request):
	""" display the newsroom main page """
	template = 'articles/newsroom/index.html'

	mediaresults = MediaResult.objects.filter(sort_order__gt=0).order_by('sort_order')[:4]
	trendingtopics = TrendingTopic.objects.filter(sort_order__gt=0).order_by('sort_order')[:3]

	ctx = {
		'mediaresults': mediaresults,
		'trendingtopics': trendingtopics,
	}

	return render(request, template, ctx)

def trendingtopics_list(request):
	""" display all active trending topics """
	template = 'articles/newsroom/trendingtopics_list.html'
	trendingtopics = TrendingTopic.objects.all().order_by('sort_order')

	ctx = {
		'trendingtopics': trendingtopics,
	}

	return render(request, template, ctx)


def mediaresults_list(request, page=1):
	""" display all active mediaresults """
	template = 'articles/newsroom/mediaresults_list.html'

	if request.user.is_authenticated():
		articles = MediaResult.qa_objects.all().order_by('-posting_time')
	else:
		articles = MediaResult.objects.all().order_by('-posting_time')

	paginator = DiggPaginator(articles, ARTICLES_PER_PAGE)

	try:
		paged_articles = paginator.page(page)
	except (EmptyPage, InvalidPage):
		paged_articles = paginator.page(paginator.num_pages)

	ctx = {
		'page': paged_articles,
		'url': '/recentcoverage/',
	}

	return render(request, template, ctx)


def mediaresults_detail(request, urlname):
	""" display mediaresult detail """
	template = 'articles/newsroom/mediaresults_details.html'
	mediaresult = get_object_or_404(MediaResult, urlname=urlname)
	trendingtopics = TrendingTopic.objects.filter(sort_order__gt=0).order_by('sort_order')[:3]

	ctx = {
		'article': mediaresult,
		'trendingtopics': trendingtopics,
	}

	return render(request, template, ctx)


def recentnews(request):
	""" display the recent news same as the newsroom main page """
	template = 'articles/newsroom/recentnews.html'

	recentnews_items = Article.objects.filter(headline_promo__gt=0).order_by('headline_promo')
	trendingtopics = TrendingTopic.objects.filter(sort_order__gt=0).order_by('sort_order')[:3]

	ctx = {
		'mediaresults': recentnews_items,
		'trendingtopics': trendingtopics,
	}

	return render(request, template, ctx)
