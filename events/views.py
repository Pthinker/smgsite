import re
import json
from datetime import datetime, date

from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Max, Min, Count
from django import forms

from smgsite.settings import CACHE_TIME
from smgsite.events.models import Event, Eventtime, Registration, Referrer, Class
from smgsite.cms.models import INCLUDE
from smgsite.events.forms import EventForm


def events(request):
	"""
	This renders the events listing page.
	"""
	today = date.today()
	if request.user.is_authenticated():
		eventtimes = Eventtime.qa_objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	else:
		eventtimes = Eventtime.objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	finallist = []
	for eventtime in eventtimes:
		if eventtime.event.active == u'1' and (request.user.is_authenticated() or eventtime.event.for_update <= 1):
			finallist.append(eventtime)
	classes = Class.objects.order_by('startdate', 'starttime')
	return render_to_response('site/events.html', {'eventtimes': finallist, 'classes': classes}, context_instance=RequestContext(request))


def event(request, event):
	"""
	This renders the event detail page.
	"""
	try:
		if request.user.is_authenticated():
			event = Event.qa_objects.get(urlname=event)
		else:
			event = Event.display_objects.get(urlname=event)
	except Event.DoesNotExist:
		raise Http404
	today = date.today()
	if request.user.is_authenticated():
		eventtimes = Eventtime.qa_objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	else:
		eventtimes = Eventtime.objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	finallist = []
	for eventtime in eventtimes:
		if eventtime.event.active == u'1' and (request.user.is_authenticated() or eventtime.event.for_update <= 1):
			finallist.append(eventtime)
	return render_to_response('site/event.html', {'event': event, 'eventtimes': finallist}, context_instance=RequestContext(request))
	
	
def classes(request):
	"""
	This renders the class listing page.
	"""
	if request.user.is_authenticated():
		classes = Class.qa_objects.order_by('startdate', 'starttime')
	else:
		classes = Class.objects.order_by('startdate', 'starttime')
	today = date.today()
	if request.user.is_authenticated():
		eventtimes = Eventtime.qa_objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	else:
		eventtimes = Eventtime.objects.filter(startdate__gte=today).order_by('startdate', 'starttime')
	finallist = []
	for eventtime in eventtimes:
		if eventtime.event.active == u'1' and (request.user.is_authenticated() or eventtime.event.for_update <= 1):
			finallist.append(eventtime)
	return render_to_response('site/classes.html', {'eventtimes': finallist, 'classes': classes}, context_instance=RequestContext(request))


def display_class(request, class_id):
	"""
	This renders the class detail page.
	"""
	try:
		if request.user.is_authenticated():
			class_q = Class.qa_objects.get(urlname=class_id)
		else:
			class_q = Class.objects.get(urlname=class_id)
	except Class.DoesNotExist:
		raise Http404
	if request.user.is_authenticated():
		classes = Class.qa_objects.order_by('startdate', 'starttime')
	else:
		classes = Class.objects.order_by('startdate', 'starttime')	
	return render_to_response('site/class.html', {'class': class_q, 'classes': classes}, context_instance=RequestContext(request))


def register(request):
	if request.REQUEST.get('eventtimes'):
		eventtimes = [long(et) for et in request.GET.get('eventtimes').split(',')]
		eventdates = Eventtime.objects.filter(startdate__gte=datetime.now()).order_by('startdate', 'starttime')
		EventForm.base_fields['eventdates'] = forms.MultipleChoiceField(choices=[(e.id, u'%s (%s)' % (e.event.title, e.timelong()), e.event.get_absolute_url(), True if e.id in eventtimes else False) for e in eventdates if e.event.exclude_from_registration == INCLUDE], widget=forms.CheckboxSelectMultiple())
	#EventForm.base_fields['events'] = forms.MultipleChoiceField(choices=[(e.id, '%s' % (e.title)) for e in Event.objects.filter(exclude_from_registration=0).filter(eventtime__startdate__gte=date.today()).annotate(max_date=Max('eventtime__startdate'), max_time=Max('eventtime__starttime')).order_by('max_date', 'max_time')], widget=forms.CheckboxSelectMultiple)
	#EventForm.base_fields['events'] = forms.MultipleChoiceField(choices=[(e.id, '%s (%s)' % (e.title, e.timeshort())) for e in Event.objects.filter(exclude_from_registration=0).filter(startdate__gte=date.today()).order_by('startdate')], widget=forms.CheckboxSelectMultiple)
	if request.method == 'POST':
		EventForm.base_fields['eventdates'] = forms.MultipleChoiceField(choices=[(e.id, u'%s (%s)' % (e.event.title, e.timelong())) for e in eventdates], widget=forms.CheckboxSelectMultiple())
		form = EventForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			referrer = Referrer.objects.get(name=data['referrer'])
			r = Registration(first_name=data['first_name'], last_name=data['last_name'], age=data['age'], city=data['city'], state=data['state'], zipcode=data['zipcode'], email=data['email'], main_phone=data['main_phone'], alt_phone=data['alt_phone'], sendmail=data['sendmail'], referrer=referrer, entered_by='U')
			r.save()
			eventdates = []
			for eid in data['eventdates']:
				v = Eventtime.objects.get(pk=eid)
				r.eventtimes.add(v)
				eventdates.append(v)
			r.save()
			return render_to_response('site/event_registered.html', {'eventtimes': eventdates}, context_instance=RequestContext(request))
		else:
			return render_to_response('site/event_registration.html', {'form': form}, context_instance=RequestContext(request))
	else:
		# Is this even used??
		eventid = request.GET.get('event')
		if eventid:
			try:
				event = Event.objects.get(pk=eventid)
				form = EventForm(initial={'events': [event.id]})
			except Event.DoesNotExist:
				form = EventForm()
		else:
			form = EventForm()
		return render_to_response('site/event_registration.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def admin_events(request):
	events_upcoming = Eventtime.objects.filter(startdate__gte=datetime.now()).order_by('startdate', 'starttime')
	events_archived = Eventtime.objects.filter(startdate__lt=datetime.now()).order_by('-startdate', '-starttime')
	return render_to_response('admin/events/registration/events.html', {'events_upcoming': events_upcoming, 'events_archived': events_archived}, context_instance=RequestContext(request))

@login_required
def admin_registrations(request):
	pk = request.GET.get('event')
	event = None
	if not pk:
		registrations = []
		for e in Event.all_objects.all():
			for t in e.eventtime_set.all():
				for r in t.registration_set.all():
					registrations.append(r)
	else:
		event = Event.all_objects.get(pk=pk)
		registrations = []
		for t in event.eventtime_set.all():
			for r in t.registration_set.all():
				registrations.append(r)
	return render_to_response('admin/events/registration/registrations.html', {'event': event, 'registrations': registrations}, context_instance=RequestContext(request))

@login_required
def export(request, data):
	if data == 'unique':
		registrations = dict()
		for registration in Registration.objects.all().order_by('-signup_date'):
			key = '%s-%s-%s' % (registration.last_name, registration.first_name, registration.email)
			if not key in registrations:
				registrations[key] = registration
		registrations = [registrations[key] for key in registrations.keys()]
		return render_to_response('admin/events/registration/export_registrations.html', {'registrations': registrations}, context_instance=RequestContext(request), mimetype='application/ms-excel')
	elif data == 'upcoming':
		eventtimes = Eventtime.objects.filter(startdate__gte=datetime.now()).order_by('startdate')
	elif data == 'archived':
		eventtimes = Eventtime.objects.filter(enddate__lt=datetime.now())
	elif data == 'event':
		pk = request.GET.get('event')
		e = Event.all_objects.get(pk=pk)
		eventtimes = Eventtime.all_objects.filter(event=e)
	else:
		return HttpResponseRedirect('/admin/events/registration/')
	return render_to_response('admin/events/registration/export_events.html', {'eventtimes': eventtimes}, context_instance=RequestContext(request), mimetype='application/ms-excel')

@login_required
def clone(request, event):
	event = Event.all_objects.get(pk=event)
	event_clone = event.clone()
	event_clone.title = "Copy of %s" % (event_clone.title)
	event_clone.save(False)
	return HttpResponseRedirect('/admin/events/event/%s/' % (event_clone.pk))



def event_stream(request, start_date, end_date):
	"""
		count of events by day for the front page calendar (from when events start) - json format.
	"""
	events = Eventtime.objects.filter(startdate__range=[start_date, end_date]).values('startdate').annotate(count=Count('startdate'))
	data = [{'title': e['count'], 'start': e['startdate'].isoformat()} for e in events]
	return HttpResponse(json.dumps(data), mimetype="application/json")


from smgsite.site.templatetags.helpers import _monthly_events_from_date

def events_monthly(request, date, count):
	"""
		Get x events for a month and render to an indivdual template block
		to be rendered using AJAX
	"""
	events = _monthly_events_from_date(int(count), datetime.strptime(date, "%Y-%m-%d").date())
	ctx = {
		'eventtimes': events,
	}
	return render_to_response('helpers/events.html', ctx, context_instance=RequestContext(request))







