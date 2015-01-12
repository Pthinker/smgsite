import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..', '..')) # project root
sys.path.append(curdir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smgsite.settings")
from django.conf import settings

import datetime, time
from django.db import transaction
from urllib import urlopen
from xml.dom.minidom import parseString
from smgsite.healthday.models import Article, Topic

@transaction.commit_on_success
def load_articles():
	
	url = urlopen('http://summit:thayer0225@www.healthday.com/wwwroot/summit/newsfeed_daily_t.dat')
	xml_data = url.read()
	dom = parseString(xml_data)
	for article in dom.getElementsByTagName('ARTICLE'):
		print "Loading article" + article.getAttribute('ID')
		article_id = article.getAttribute('ID')
		posting_date = article.getAttribute('POSTING_DATE')
		posting_time = posting_date + " " + article.getAttribute('POSTING_TIME')
		posting_time = datetime.datetime(*time.strptime(posting_time, "%d-%b-%Y %H:%M")[0:5])
		archive_date = article.getAttribute('ARCHIVE_DATE')
		archive_date = datetime.datetime(*time.strptime(archive_date, "%d-%b-%Y")[0:5])
		urlname = article_id
		values = {'article_id': article_id, 'urlname': urlname, 'posting_time': posting_time, 'archive_date': archive_date}
		for field in Article._meta.fields:
			name = field.name
			try:
				value = article.getElementsByTagName(name.upper())[0].firstChild.data
				values[name] = value
			except (AttributeError, IndexError):
				pass
		try:
			a = Article.objects.get(article_id=article_id)
			a.delete()
		except Article.DoesNotExist:
			pass
		a = Article(**values)
		a.save()
		for topic in article.getElementsByTagName('TOPIC'):
			try:
				t = Topic.objects.get(topic=topic.getAttribute('ID'))
				a.topics.add(t)
			except Topic.DoesNotExist:
				print "Unable to locate topic", topic.getAttribute('ID')

load_articles()
