#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('smgsite.cms.views',
    ('^$', 'index'),
	(r'^change/(?P<pk>.*)/$', 'change'),
	(r'^unchange/(?P<pk>.*)/$', 'unchange'),
	(r'^add/(?P<app>.*)/(?P<model>.*)/(?P<pk>.*)/$', 'add'),
	(r'^delete/(?P<app>.*)/(?P<model>.*)/(?P<pk>.*)/$', 'delete')
)
