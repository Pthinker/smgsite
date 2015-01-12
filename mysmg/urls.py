#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include

urlpatterns = patterns('smgsite.mysmg.views',
	(r'^$', 'home'),
	(r'^my_library/$', 'view'),
	(r'^register/confirm/$', 'confirm'),
	(r'^register/$', 'register'),
	(r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
	(r'^forgot/$', 'forgot'),
	(r'^edit/$', 'edit'),
	(r'^password-reset/$', 'reset'),
	(r'^add/$', 'add'),
)
