#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page

CACHE_TIME = getattr(settings, 'CACHE_TIME', 60 * 60)

admin.autodiscover()

#handler404 = 'smgsite.pages.views.dispatch'

from smgsite.doctors.search_views import MultiFacetedSearchView, MultiFacetedSearchForm, get_sqs
from smgsite.search.search_views import FullSearchView
from haystack.views import search_view_factory


urlpatterns = patterns('',

	# minisite news display
	(r'^service/Oncology-Center/News/News-Items/(?P<page>.*)/$',  
		'smgsite.healthday.views.news_by_category',
		{'category_pk':1, 
		'template':'pages/oncologycenternews.html', 
		'url':'/service/Oncology-Center/News/News-Items/',
		'contentpath': 'News-Items'}),

	# This is a hack to work with the admin file browser
	(r'^fckconnector$', 'smgsite.editor.views.fckbrowser'),
	(r'^media/fckeditor/editor/filemanager/connectors/php/connector.php$', 'smgsite.editor.views.fckbrowser'),
	
	# TODO: is this a good idea?
	# This is required for admin scripts that change page content
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	# Dynamic CSS Generation
	(r'^dynamic-css/(?P<template>.*)$', 'smgsite.site.views.dynamic_css'),
	

	# Content Management System links
	(r'^admin/cms/', include('smgsite.cms.urls')),
	(r'^admin/cms/keywords/', 'smgsite.cms.views.keywords'),
	
	(r'^admin/events/registration/export/(?P<data>.*)/event_registrations.csv$', 'smgsite.events.views.export'),
	(r'^admin/events/registration/list/$', 'smgsite.events.views.admin_registrations'),
	(r'^admin/events/registration/$', 'smgsite.events.views.admin_events'),
	(r'^admin/events/clone/(?P<event>.*)/$', 'smgsite.events.views.clone'),
	(r'^admin/mysmg/user/export/users.csv$', 'smgsite.mysmg.views.export'),
	(r'^admin/articles/article/reorder/$', 'smgsite.articles.views.admin_article_reorder'),
	(r'^admin/articles/article/set-reorder/$', 'smgsite.articles.views.admin_set_article_reorder'),
	#(r'^admin/doctors/bulk-entry/$', 'smgsite.doctors.views.bulk_entry'),
	(r'^admin/doctors/specialty-export.csv$', 'smgsite.doctors.views.specialty_export'),
	(r'^admin/doctors/no-specialty-export.csv$', 'smgsite.doctors.views.no_specialty_export'),
	(r'^admin/doctors/doctor/accepting/$', 'smgsite.doctors.views.admin_accepting'),
	(r'^admin/doctors/doctor/set-accepting/$', 'smgsite.doctors.views.admin_set_accepting'),
	(r'^admin/services/bulk-entry/$', 'smgsite.services.old_views.bulk_entry'),
	(r'^admin/site/unsubscribe/export/unsubscribe.csv$', 'smgsite.site.views.export_unsubscribe'),
	(r'^admin/articles/mediaresult/reorder/$', 'smgsite.articles.views.admin_mediaresult_reorder'),
	(r'^admin/articles/mediaresult/set-reorder/$', 'smgsite.articles.views.admin_set_mediaresult_reorder'),
	
	# Uncomment this for admin:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', admin.site.urls),

	# Redirects
	(r'^(extensivist)/', 'smgsite.redirect.views.redirect'),
	(r'^(bp)/', 'smgsite.redirect.views.redirect'),
	
	# Editor System links
	(r'^editor/', include('smgsite.editor.urls')),
	
	# Search System links
	#(r'^search/', search_view_factory(view_class=FullSearchView)),
	(r'^search/', include('smgsite.search.urls')),

	# Blog links
	(r'^blogs/', 'smgsite.blogs.views.index'),
	(r'^blog/', include('smgsite.blogs.urls')),
	
	# MySMG links
	#(r'^mysummitmedicalgroup/', include('smgsite.mysmg.urls')),
	
	# Site links
	(r'^$', 'smgsite.site.views.index'),
	(r'^test/$', 'smgsite.site.views.index_test'),
	
	(r'^about/$', 'smgsite.site.views.about_index'),
	(r'^about/(?P<path>.*)/$', 'smgsite.site.views.about_page'),

	(r'^locations/$', 'smgsite.site.views.locations'),
	(r'^locations/all/$', 'smgsite.site.views.locations_all'),
	#(r'^locations/transportation/$', 'smgsite.site.views.locations_redirect'),
	#(r'^location/hours_popup/(?P<location>.*)/$', 'smgsite.site.views.location_hours_popup'),
	(r'^location/(?P<location>.*)/$', 'smgsite.site.views.location'),
	
	(r'^events/$', 'smgsite.events.views.events'),
	(r'^events/registration/$', 'smgsite.events.views.register'),
	(r'^event/(?P<event>.*)/$', 'smgsite.events.views.event'),
	(r'^events/stream/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)/$', 'smgsite.events.views.event_stream'),
	(r'^events/monthly/(?P<date>[-\w]+)/(?P<count>\d+)/$', 'smgsite.events.views.events_monthly'),
	
	(r'^classes/$', 'smgsite.events.views.classes'),
	(r'^class/(?P<class_id>.*)/$', 'smgsite.events.views.display_class'),
	
	
	
	url(r'^doctors/', include('smgsite.doctors.urls')),

	# outside of /doctors/ includes as it doesn't follow pattern
	(r'^doctor-directory/$', cache_page(CACHE_TIME)(search_view_factory(
		view_class=MultiFacetedSearchView,
		form_class=MultiFacetedSearchForm,
		template='doctors/results_text.html',
		searchqueryset=get_sqs()))),

	(r'^doctor-finder/$', 'smgsite.doctors.views.doctor_finder'),
	(r'^doctor-specialty/$', 'smgsite.doctors.views.doctor_specialty'),

	(r'^doctor/(?P<doctor>.*)/$', 'smgsite.doctors.views.doctor'),

	(r'^doctor-survey-index$', 'smgsite.doctors.views.doctor_survey_index'),
	(r'^doctor-survey-submit$', 'smgsite.doctors.views.doctor_survey_submit'),
	(r'^doctor-survey$', 'smgsite.doctors.views.doctor_survey'),


	url(r'^service/', include('smgsite.services.urls'), name='services'),
	url(r'^services/$', 'smgsite.services.views.service_groups_view', name="service-groups"),
    url(r'^services/all/$', 'smgsite.services.views.services_view'),

	#(r'^services/$', 'smgsite.services.old_views.index'),
	#(r'^service/(?P<service>.*?)/(?P<subservice>.*)/$', 'smgsite.services.old_views.subservice'),
	#(r'^service/(?P<service>.*)/$', 'smgsite.services.old_views.service'),

	(r'^articles/$', 'smgsite.articles.views.index'),
	(r'^article-leader/(?P<position>.*)/$', 'smgsite.articles.views.leader'),	
	(r'^articles/(?P<page>.*)/$', 'smgsite.articles.views.index'),
	(r'^article/(?P<urlname>.*)/$', 'smgsite.articles.views.article'),

	
	#(r'^press-releases/year/(?P<year>.*?)/(?P<page>.*)/$', 'smgsite.articles.views.pr_index'),
	#(r'^press-releases/year/(?P<year>.*)/$', 'smgsite.articles.views.pr_index'),
	#(r'^press-releases/$', 'smgsite.articles.views.pr_index'),	
	#(r'^press-release/(?P<urlname>.*)/$', 'smgsite.articles.views.press_release'),


	(r'^features/(?P<content>[-\w]+)/$', 'smgsite.articles.views.features'),
	(r'^features/(?P<content>[-\w]+)/(?P<page>\d+)/$', 'smgsite.articles.views.features'),
	(r'^feature/(?P<content>[-\w]+)/(?P<urlname>.*)/$', 'smgsite.articles.views.feature'),

	(r'^recipes/$', 'smgsite.articles.views.recipes'),
	(r'^recipes/(?P<page>.*)/$', 'smgsite.articles.views.recipes'),
	(r'^recipe/(?P<urlname>.*)/$', 'smgsite.articles.views.recipe'),

	(r'^healthyconnections/$', 'smgsite.articles.views.pdfs'),

	(r'^healthday/article/(?P<urlname>.*)/$', 'smgsite.healthday.views.article'),	
	(r'^healthday/$', 'smgsite.healthday.views.landing'),
	(r'^healthday/rss/$', 'smgsite.healthday.views.rss'),
	(r'^healthday/rss-type/(?P<news_type>.*)/$', 'smgsite.healthday.views.type_rss'),
	(r'^healthday/rss-topic/(?P<topic>.*)/$', 'smgsite.healthday.views.topic_rss'),
	(r'^healthday/rss-category/(?P<category>.*)/$', 'smgsite.healthday.views.category_rss'),
	(r'^healthday/(?P<news_type>.*)/(?P<page>.*)/$', 'smgsite.healthday.views.index'),

	(r'^library/id/(?P<article_id>.*)/$', 'smgsite.relayhealth.views.article_id'),
	(r'^library/(?P<advisor>.*)/(?P<article>.*)/$', 'smgsite.relayhealth.views.article'),
	(r'^library/(?P<advisor>.*)/$', 'smgsite.relayhealth.views.advisor'),
	(r'^library/$', 'smgsite.relayhealth.views.index'),
	
	(r'^email-page/$', 'smgsite.site.views.email_page'),
	
	(r'^careers/$', 'smgsite.careers.views.careers_search'),
	
	(r'^news(?P<number>\d+)/$', 'smgsite.site.views.promotion'),
	
	(r'^slider/$', 'smgsite.site.views.slider'),
	(r'^mainvideo/$', 'smgsite.site.views.mainvideo'),

	# Unsubscribe feature
	(r'^site/unsubscribe/$', 'smgsite.site.views.unsubscribe'),

	# Minisites
	(r'^minisite-test/$', 'smgsite.minisite.views.test'),

	#Newsroom
	(r'^newsroom/$', 'smgsite.articles.views.newsroom_index'),
	(r'^trendingtopics/$', 'smgsite.articles.views.trendingtopics_list'),
	(r'^recentcoverage/$', 'smgsite.articles.views.mediaresults_list'),
	
	(r'^recentcoverage/$', 'smgsite.articles.views.mediaresults_list'),
	(r'^recentcoverage/(?P<page>\d+)/$', 'smgsite.articles.views.mediaresults_list'),
	(r'^recentcoverage/(?P<urlname>[-\w]+)/$', 'smgsite.articles.views.mediaresults_detail'),
	(r'^recentnews/$', 'smgsite.articles.views.recentnews'),


)

if settings.DEBUG:
	from django.views.generic import TemplateView
	urlpatterns += patterns('',
		url(r'^404/$', TemplateView.as_view(template_name='404.html')),
		url(r'^500/$', TemplateView.as_view(template_name='500.html')),
)
