from datetime import datetime, date
from django.http import Http404
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response
from django.db.models import Q
from django import forms
from django.forms.formsets import formset_factory

from math import ceil
from datetime import date

from smgsite.settings import CACHE_TIME, TEMPLATE_ROOT, MEDIA_URL
from smgsite.services.models import Service, Link_Nav, Link_Body, Location, ServiceGroup
from smgsite.events.models import Event, Eventtime
from smgsite.doctors.models import Doctor
from smgsite.search.interface import title_re
import smgsite.site.models as site
from smgsite.services.forms import ServiceForm

import re

media_re = re.compile(r'(<img[^>]+src=\")/media')


class RowList(object):
	def __init__(self, letter, rows):
		self.letter = letter
		self.rows = rows


def index(request):
	"""
	This renders the service index page.
	"""
	if request.user.is_authenticated():
		services = Service.qa_objects.order_by('name')
	else:
		services = Service.objects.order_by('name')
	# List by letter
	pos = 0
	letters = []
	while pos < len(services):
		letter = services[pos].letter_key()
		x = pos
		while x < len(services) and letter == services[x].letter_key():
			x += 1
		count = x - pos
		offset = 0
		rows = []
		row = []
		for service in services[pos:pos+count]:
			if offset == 4:
				rows.append(row)
				row = []
				offset = 0
			row.append(service)
			offset += 1
		rows.append(row)
		letters.append(RowList(letter, rows))
		pos = pos + count
	return render_to_response('services/services.html', {'services': services, 'letters': letters}, context_instance=RequestContext(request))

def service(request, service):
	"""
	This renders the service display page.
	"""
	if request.user.is_authenticated():
		try:
			service = Service.qa_objects.get(urlname=service)
		except Service.DoesNotExist:
			service = Service.qa_objects.get(aliases__urlname=service)
		service.qa = True
		events = Event.qa_objects.filter(service=service, eventtime__startdate__gte=date.today())
		today = date.today()
		eventtimes = Eventtime.qa_objects.filter(event__in=events, startdate__gte=today).order_by('startdate','starttime')
		doctors = Doctor.qa_objects.order_by('last_name').filter(status='D').filter(Q(title_service=service) | Q(services=service)).distinct()
		staff = Doctor.qa_objects.order_by('last_name').filter(status='S').filter(Q(title_service=service) | Q(services=service)).distinct()
	else:
		try:
			service = Service.objects.get(urlname=service)
		except Service.DoesNotExist:
			try:
				service = Service.objects.get(aliases__urlname=service)
			except Service.DoesNotExist:
				raise Http404
		service.qa = False
		events = Event.objects.filter(service=service, eventtime__startdate__gte=date.today())
		today = date.today()
		eventtimes = Eventtime.objects.filter(event__in=events, startdate__gte=today).order_by('startdate', 'starttime')
		doctors = Doctor.objects.order_by('last_name').filter(status='D').filter(Q(title_service=service) | Q(services=service)).distinct()
		staff = Doctor.objects.order_by('last_name').filter(status='S').filter(Q(title_service=service) | Q(services=service)).distinct()
	template = 'services/%s' % service.template.name
	content = media_re.sub('\\1%s' % MEDIA_URL, service.content)
	offerings = media_re.sub('\\1%s' % MEDIA_URL, service.offerings)
	learn_more = media_re.sub('\\1%s' % MEDIA_URL, service.learn_more)
	patient_tools = media_re.sub('\\1%s' % MEDIA_URL, service.patient_tools)
	return render_to_response(template, {'service': service, 'doctors': doctors, 'staff': staff, 'events': events, 'eventtimes': eventtimes, 'content': content, 'offerings': offerings, 'learn_more': learn_more, 'patient_tools': patient_tools}, context_instance=RequestContext(request))

# TODO: this should probably be cleaned up and moved to views.py
# It would be better to use an updated pages model that uses full unique paths
def subservice(request, service, subservice):
	from smgsite.pages.models import Template, Directory, Page
	"""
	This renders the subservice display page.
	"""
	path = 'service/%s/%s' % (service, subservice)
	path = path.strip('/').split('/')
	pathdir = '/'.join(path[0:-1])
	pathfile = path[-1]
	print "Pathdir is %s" % pathdir
	print "Pathfile is %s" % pathfile
	if request.user.is_authenticated():
		try:
			service = Service.qa_objects.get(urlname=service)
		except Service.DoesNotExist:
			service = Service.qa_objects.get(aliases__urlname=service)
		service.qa = True
		directory = Directory.objects.get(directory=pathdir)
		events = Event.qa_objects.filter(service=service)
		doctors = Doctor.qa_objects.order_by('last_name').filter(status='D').filter(Q(title_service=service) | Q(services=service)).distinct()
		staff = Doctor.qa_objects.order_by('last_name').filter(status='S').filter(Q(title_service=service) | Q(services=service)).distinct()
	else:
		service = Service.objects.get(urlname=service)
		service.qa = False
		try:
			directory = Directory.objects.get(directory=pathdir)
		except Directory.DoesNotExist:
			raise Http404
		events = Event.objects.filter(service=service)
		doctors = Doctor.objects.order_by('last_name').filter(status='D').filter(Q(title_service=service) | Q(services=service)).distinct()
		staff = Doctor.objects.order_by('last_name').filter(status='S').filter(Q(title_service=service) | Q(services=service)).distinct()
	offerings = media_re.sub('\\1%s' % MEDIA_URL, service.offerings)
	learn_more = media_re.sub('\\1%s' % MEDIA_URL, service.learn_more)
	patient_tools = media_re.sub('\\1%s' % MEDIA_URL, service.patient_tools)
	try:
		if request.user.is_authenticated():
			page = Page.qa_objects.get(directory=directory, urlname=pathfile)
		else:
			page = Page.objects.get(directory=directory, urlname=pathfile)
	except Page.DoesNotExist:
		raise Http404
	template = 'pages/%s' % directory.template.name
	content = media_re.sub('\\1%s' % MEDIA_URL, page.content)
	ctx = {
		'page': page, 
		'content': content, 
		'service': service, 
		'doctors': doctors, 
		'staff': staff, 
		'events': events, 
		'content': content, 
		'offerings': offerings, 
		'learn_more': learn_more, 
		'patient_tools': patient_tools, 
		'subservice': subservice,
		'quicklook_form': ServiceForm(),
        'service_groups': ServiceGroup.objects.all(),
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))



"""
Service bulk import form for locations.

This is a temporary form to gather new location data for
the Fall 2011 location enhancement launch.
"""

class ReadOnlyWidget(forms.Widget):
	def render(self, name, value, attrs):
		final_attrs = self.build_attrs(attrs, name=name)
		if hasattr(self, 'initial'):
			value = self.initial
		return value

	def _has_changed(self, initial, data):
		return False


class LocationDataForm(forms.Form):
	existing = forms.CharField(required=False, widget=ReadOnlyWidget())
	pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
	name = forms.CharField(required=False, widget=ReadOnlyWidget())
	location = forms.ModelChoiceField(required=False, queryset=site.Location.objects.all())
	position = forms.IntegerField(required=False)
	extra1 = forms.CharField(required=False)
	extra2 = forms.CharField(required=False)
	extra3 = forms.CharField(required=False)

@login_required
def bulk_entry(request):
	if request.method == 'POST':
		ArticleFormSet = formset_factory(LocationDataForm, extra=0)
		formset = ArticleFormSet(request.POST)
		if formset.is_valid():
			for form in formset.forms:
				try:
					location = form.cleaned_data['location']
				except KeyError:
					location = None
				if location:
					try:
						service = Service.all_objects.get(pk=form.cleaned_data['pk'])
						location = form.cleaned_data['location']
						position = form.cleaned_data['position']
						extra1 = form.cleaned_data['extra1']
						extra2 = form.cleaned_data['extra2']
						extra3 = form.cleaned_data['extra3']
						locobj = Location(service=service, location=location, position=position, extra1=extra1, extra2=extra2, extra3=extra3)
						service.location_set.add(locobj)
						service.save(preview=False)
					except service.DoesNotExist:
						pass
	ArticleFormSet = formset_factory(LocationDataForm, extra=0)
	initial = []
	for s in Service.all_objects.order_by('name'):
		loc = ''
		for l in s.location_set.all():
			loc += "%s %s %s %s<br />" % (l.location.name, l.extra1, l.extra2, l.extra3)
		initial.append({'pk': s.pk, 'name': s.name, 'existing': loc})
	formset = ArticleFormSet(initial=initial)
	return render_to_response('admin/services/bulk-input.html', {'formset': formset}, context_instance=RequestContext(request))
