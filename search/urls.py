#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

from smgsite.search.search_views import FullSearchView, ModelSearchView
from haystack.views import search_view_factory

urlpatterns = patterns('smgsite.search.views',
	(r'^ajax/(?P<kind>.*)/(?P<model>.*)/(?P<order>.*)/$', 'ajax_solr_search'),
	(r'^model/$', search_view_factory(view_class=ModelSearchView)),
	(r'^$', search_view_factory(view_class=FullSearchView)),
)
