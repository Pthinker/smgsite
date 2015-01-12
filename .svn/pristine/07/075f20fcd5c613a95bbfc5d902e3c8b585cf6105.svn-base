from django.conf.urls import include, url
from django.conf.urls import patterns, url, include




urlpatterns = patterns('', 
    url(r'^group/(?P<urlname>[-\w]+)/$', 'smgsite.services.views.service_group_view', name="service-group"),
    url(r'^(?P<urlname>[-\w]+)/$', 'smgsite.services.views.service_detail_view', name="service-detail"),
    (r'^(?P<service>.*?)/(?P<subservice>.*)/$', 'smgsite.services.old_views.subservice'),
    (r'^(?P<service>.*)/$', 'smgsite.services.old_views.service'),
)