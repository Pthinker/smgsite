import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..'))
sys.path.append(curdir)
from django.core.management import setup_environ
import settings
setup_environ(settings)

import re
import urllib2
import time
from datetime import datetime
from smgsite.articles.models import PressRelease

date_re = re.compile(r'<li>([^:]+): <a href="/about/Press_Room/([^"]+)/"')

url = 'http://www.summitmedicalgroup.com/about/Press_Room/'
try:
	f = urllib2.urlopen(url)
	page = f.read()
	for match in date_re.finditer(page):
		datestr = match.group(1)
                date = datetime(*time.strptime(datestr, '%B %d, %Y')[0:5])
		urlname = match.group(2)
		print '%s -> %s' % (date, urlname)
		try:
			release = PressRelease.objects.get(urlname=urlname)
			release.posting_time = date
			release.display_time = date
			release.save(preview=False)
		except PressRelease.DoesNotExist:
			print "Not found!"
except urllib2.HTTPError:
	print 'HTTP Error on %s' % url
except urllib2.URLError:
	print 'URL Error on %s' % url

