#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('smgsite.blogs.views',
	(r'^admin/$', 'admin'),
	(r'^admin/post/(?P<urlname>.*)/$', 'blogEdit'),
	(r'^admin/(?P<urlname>.*)/$', 'blogAdmin'),
	(r'^rss/(?P<blog>.*)/$', 'rss'),
	(r'^landing/(?P<urlname>.*)/$', 'full_listing'),
	(r'^(?P<blog>.*)/(?P<urlname>.*)/$', 'post'),
	(r'^(?P<urlname>.*)/$', 'listing'),
)
