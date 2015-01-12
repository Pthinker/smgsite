#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('smgsite.editor.views',
    ('^$', 'index'),
    ('^dir/(?P<path>.*)/(?P<message>.*)$', 'path_index'),
    ('^view/(?P<path>.*)$', 'view'),
    ('^source/(?P<path>.*)$', 'source'),
    ('^edit/(?P<path>.*)$', 'edit'),
    ('^newdir/$', 'newdir'),
    ('^new/$', 'new'),
	#(r'^change/(?P<pk>.*)/$', 'change'),
	#(r'^add/(?P<app>.*)/(?P<model>.*)/(?P<pk>.*)/$', 'add'),
	#(r'^delete/(?P<app>.*)/(?P<model>.*)/(?P<pk>.*)/$', 'delete')

)
