from django.conf.urls import include, url
from django.conf.urls import patterns, url, include
from django.views.decorators.cache import cache_page
from django.conf import settings

from smgsite.doctors.search_views import MultiFacetedSearchView, MultiFacetedSearchForm, get_sqs

from haystack.views import search_view_factory

CACHE_TIME = getattr(settings, 'CACHE_TIME', 60 * 5)

urlpatterns = patterns('',
    #(r'^$', 'smgsite.doctors.views.doctor_finder'),
    (r'^$', cache_page(CACHE_TIME)(search_view_factory(
        view_class=MultiFacetedSearchView,
        form_class=MultiFacetedSearchForm,
        searchqueryset=get_sqs()))),
)