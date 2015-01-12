from math import ceil
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from smgsite.settings import CACHE_TIME
from smgsite.relayhealth.models import Article, Advisor


class ColumnList(object):
	def __init__(self, section, count, thelist):
		self.section = section
		self.count = count
		self.thelist = thelist
	def first_column(self):
		return self.thelist[0:self.count]
	def second_column(self):
		return self.thelist[self.count:]


def article_id(request, article_id):
	"""
	This redirects to the article display page.
	"""
	article = Article.objects.get(article_id=article_id)
	(advisor, article) = article.urlname.split('/')
	return HttpResponseRedirect(reverse('smgsite.relayhealth.views.article', args=(advisor, article)))


def article(request, advisor, article):
	"""
	This renders the article display page.
	"""
	urlname = '%s/%s' % (advisor, article)
	try:
		article = Article.objects.get(urlname=urlname)
	except:
		return index(request, notfound=True)
		#raise Http404
	return render_to_response('articles/relayhealth.html', {'article': article}, context_instance=RequestContext(request))


def advisor(request, advisor):
	"""
	This renders the advisor-level library index page.
	"""
	try:
		advisor = Advisor.objects.get(urlname=advisor)
		articles = Article.objects.order_by('title').filter(reference=False, advisor=advisor)
		# List by letter
		pos = 0
		letters = []
		while pos < len(articles):
			letter = articles[pos].letter_key()
			x = pos
			while x < len(articles) and letter == articles[x].letter_key():
				x += 1
			count = x - pos
			c = int(ceil(float(count) / 2))
			letters.append(ColumnList(letter, c, articles[pos:pos+count]))
			pos = pos + count
		return render_to_response('articles/relayhealth-advisor.html', {'advisor': advisor, 'articles': articles, 'letters': letters}, context_instance=RequestContext(request))
	except:
		return index(request, notfound=True)


def index(request, notfound=False):
	"""
	This renders the top library index page.
	"""
	try:
		advisors = Advisor.objects.order_by('name')
		half = int(ceil(float(len(advisors)) / 2))
		return render_to_response('articles/relayhealth-index.html', {'advisors': advisors, 'half': half, 'notfound': notfound}, context_instance=RequestContext(request))
	except:
		return render_to_response('articles/relayhealth-update.html', {}, context_instance=RequestContext(request))

