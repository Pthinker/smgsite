from django.template import Template, RequestContext
from django.db.models import Q
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import Http404
from django import forms
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.core.cache import cache
from django.db import connection, transaction
from django.utils.html import escape, conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.encoding import smart_unicode, smart_str

from math import ceil
from urllib import quote_plus
from itertools import chain
import re
from smgsite.settings import CACHE_TIME
import smgsite.cms.models as cms
from smgsite.doctors.models import Doctor, Hospital, Language, Accreditation_name, SpecialtyUpdate
from smgsite.services.models import Service
from smgsite.site.models import Location
from smgsite.search import interface


FORM_CACHE_TIME = 60 * 60 * 2


class RowList(object):
	def __init__(self, letter, rows):
		self.letter = letter
		self.rows = rows


class ServiceList(object):
	def __init__(self, service, doctors):
		self.service = service
		self.doctors = doctors

# TODO - can this be removed?
def index(request):
	"""
	This renders the doctor index page.
	"""
	if request.user.is_authenticated():
		doctors = Doctor.qa_objects.order_by('last_name', 'first_name').exclude(exclude_from_index=cms.EXCLUDE)
	else:
		doctors = Doctor.objects.order_by('last_name', 'first_name').exclude(exclude_from_index=cms.EXCLUDE)
	if request.GET.get('service') and request.GET['service'] != 'Any':
		doctors = doctors.filter(Q(title_service=request.GET['service']) | Q(services__id=request.GET['service']))
	if request.GET.get('alpha') and request.GET['alpha'] != 'Any':
		alpha = request.GET['alpha']
		if alpha == '1':
			doctors = doctors.filter(Q(last_name__startswith='A') | Q(last_name__startswith='B') | Q(last_name__startswith='C') | Q(last_name__startswith='D'))
		elif alpha == '2':
			doctors = doctors.filter(Q(last_name__startswith='E') | Q(last_name__startswith='F') | Q(last_name__startswith='G') | Q(last_name__startswith='H'))
		elif alpha == '3':
			doctors = doctors.filter(Q(last_name__startswith='I') | Q(last_name__startswith='J') | Q(last_name__startswith='K') | Q(last_name__startswith='L'))
		elif alpha == '4':
			doctors = doctors.filter(Q(last_name__startswith='M') | Q(last_name__startswith='N') | Q(last_name__startswith='O') | Q(last_name__startswith='P'))
		elif alpha == '5':
			doctors = doctors.filter(Q(last_name__startswith='Q') | Q(last_name__startswith='R') | Q(last_name__startswith='S') | Q(last_name__startswith='T'))
		elif alpha == '6':
			doctors = doctors.filter(Q(last_name__startswith='U') | Q(last_name__startswith='V') | Q(last_name__startswith='W') | Q(last_name__startswith='X') | Q(last_name__startswith='Y') | Q(last_name__startswith='Z'))
	if request.GET.get('location') and request.GET['location'] != 'Any':
		doctors = doctors.filter(Q(location=request.GET['location']) | Q(extra_locations=request.GET['location']))
	doctors = doctors.distinct()
	# List by letter
	pos = 0
	letters = []
	while pos < len(doctors):
		letter = doctors[pos].letter_key()
		x = pos
		while x < len(doctors) and letter == doctors[x].letter_key():
			x += 1
		count = x - pos
		offset = 0
		rows = []
		row = []
		for doctor in doctors[pos:pos+count]:
			if offset == 3:
				rows.append(row)
				row = []
				offset = 0
			row.append(doctor)
			offset += 1
		rows.append(row)
		letters.append(RowList(letter, rows))
		pos = pos + count
	services = [service for service in Service.objects.all()]
	locations = [location for location in Location.objects.filter(display=Location.SHOW)]
	return render_to_response('doctors/doctors.html', {'doctors': doctors, 'letters': letters, 'services': services, 'locations': locations}, context_instance=RequestContext(request))

# TODO - can this be removed?
def index_service(request):
	"""
	This renders the doctor index page listed by specialty.
	"""
	if request.user.is_authenticated():
		doctors = Doctor.objects.order_by('title_service', 'last_name', 'first_name').exclude(exclude_from_index=True)
	else:
		doctors = Doctor.qa_objects.order_by('title_service', 'last_name', 'first_name').exclude(exclude_from_index=True)
	# List by service
	pos = 0
	services = []
	while pos < len(doctors):
		service = doctors[pos].title_service
		x = pos
		while x < len(doctors) and service == doctors[x].title_service:
			x += 1
		count = x - pos
		c = int(ceil(float(count) / 2))
		services.append(ColumnList(service, c, doctors[pos:pos+count]))
		pos = pos + count
		services.sort(lambda x, y: cmp(x.section.name, y.section.name))
	return render_to_response('doctors/doctors-by-service.html', {'services': services}, context_instance=RequestContext(request))


def doctor(request, doctor):
	"""
	This renders the doctor display page.
	"""
	try:
		if request.user.is_authenticated():
			doctor = Doctor.qa_objects.get(urlname=doctor)
			doctor.qa = True
		else:
			doctor = Doctor.objects.get(urlname=doctor)
			doctor.qa = False
		touch = Template(doctor.touch).render(RequestContext(request))
	except Doctor.DoesNotExist:
		raise Http404
	services = [service for service in Service.objects.all()]
	locations = [location for location in Location.objects.filter(display=1)]
	return render_to_response('doctors/doctor.html', {'doctor': doctor, 'touch': touch, 'services': services, 'locations': locations}, context_instance=RequestContext(request))

# TODO - can this be removed?
class DoctorFinderChoiceWidget(forms.SelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		output = [u'<ul>']
		# Normalize to strings
		str_values = set([force_unicode(v) for v in value])
		for i, (option_value, option_label, disabled) in enumerate(chain(self.choices, choices)):
			# If an ID attribute was given, add a numeric index as a suffix,
			# so that the checkboxes don't all have the same ID attribute.
			if has_id:
				final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
				label_for = u' for="%s"' % final_attrs['id']
			else:
				label_for = ''

			if disabled:
				final_attrs['disabled'] = 'disabled'
			else:
				try:
					del(final_attrs['disabled'])
				except KeyError:
					pass
			cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
			option_value = force_unicode(option_value)
			rendered_cb = cb.render(name, option_value)
			option_label = conditional_escape(force_unicode(option_label))
			output.append(u'<li class="major-indent"><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
		output.append(u'</ul>')
		return mark_safe(u'\n'.join(output))

class DoctorFinderChoiceField(forms.MultipleChoiceField):
	def validate(self, value):
		"""
		Validates that the input is a list or tuple.
		"""
		if self.required and not value:
			raise forms.ValidationError(self.error_messages['required'])
		# Validate that each value in the value list is in self.choices.
		for val in value:
			if not self.valid_value(val):
				raise forms.ValidationError(self.error_messages['invalid_choice'] % {'value': val})

	def valid_value(self, value):
		"Check to see if the provided value is a valid choice"
		for k, v, d in self.choices:
			if isinstance(v, (list, tuple)):
				# This is an optgroup, so look inside the group for options
				for k2, v2 in v:
					if value == smart_unicode(k2):
						return True
			else:
				if value == smart_unicode(k):
					return True
		return False

# TODO - can this be removed?
class DoctorFinderForm(forms.Form):
	"""
	Core for for doctor finder application
	"""
	def __init__(self, *args, **kwargs):
		super(DoctorFinderForm, self).__init__(*args, **kwargs)

	def set_choices(self, initial, doctors, location_filter=None, specialty_filter=None, gender_filter=None, languages_filter=None, hospitals_filter=None):
		if not location_filter:
			location_filter = doctors
		if not specialty_filter:
			specialty_filter = doctors
		if not gender_filter:
			gender_filter = doctors
		if not languages_filter:
			languages_filter = doctors
		if not hospitals_filter:
			hospitals_filter = doctors
		choices = None
		if initial:
			choices = cache.get('finder-locations')
		if not choices:
			choices = []
			cities = set()
			options = set()
			ls = cache.get('finder-doctor-locations')
			if ls:
				for d in location_filter:
					for l in ls[d]:
						cities.add(l.location.city)
						options.add(l.location)
			else:
				ls = dict()
				for d in location_filter:
					ls[d] = []
					for l in d.location_set.all():
						cities.add(l.location.city)
						options.add(l.location)
						ls[d].append(l)
				if initial:
					cache.set('finder-doctor-locations', ls, FORM_CACHE_TIME)
			berkeley = cache.get('finder-location-berkeley')
			if not berkeley:
				berkeley = list(Location.objects.filter(city='Berkeley Heights', display=1).values('city').order_by('city').distinct())
				cache.set('finder-location-berkeley', berkeley, FORM_CACHE_TIME)
			subberkeley = cache.get('finder-location-subberkeley')
			if not subberkeley:
				subberkeley = list(Location.objects.filter(city='Berkeley Heights', display=1).order_by('display_name'))
				cache.set('finder-location-subberkeley', subberkeley, FORM_CACHE_TIME)
			for i in berkeley:
				if i['city'] in cities:
					choices.append(((None, i['city'].replace(' ', '_')), mark_safe('<span id="form-location-val-%s">%s</span>' % (i['city'].replace(' ', '_'), i['city'])), False))
					for j in subberkeley:
						if j.display_name != '':
							name = '%s, %s' % (j.display_name, j.address)
						else:
							name = '%s' % (j.address)
						if j in options:
							choices.append((j.pk, mark_safe('<span class="form-location-sub" id="form-location-val-%s">%s</span>' % (j.pk, name)), False))
						else:
							choices.append((j.pk, mark_safe('<span style="color: #888;" class="form-location-sub" id="form-location-val-%s">%s</span>' % (j.pk, name)), True))
				else:
					choices.append(((None, i['city'].replace(' ', '_')), mark_safe('<span style="color: #888;" id="form-location-val-%s">%s</span>' % (i['city'].replace(' ', '_'), i['city'])), False))
			notberkeley = cache.get('finder-location-notberkeley')
			if not notberkeley:
				notberkeley = list(Location.objects.exclude(city='Berkeley Heights').filter(display=1).values('city').order_by('city').distinct())
				cache.set('finder-location-notberkeley', notberkeley, FORM_CACHE_TIME)
			for i in notberkeley:
				if i['city'] in cities:
					choices.append(((None, i['city'].replace(' ', '_')), mark_safe('<span id="form-location-val-%s">%s</span>' % (i['city'].replace(' ', '_'), i['city'])), False))
					snbkey = i['city'].replace(' ', '_')
					subnotberkeley = cache.get('finder-location-subnotberkeley-%s' % snbkey)
					if not subnotberkeley:
						subnotberkeley = list(Location.objects.filter(city=i['city'], display=1).order_by('display_name'))
						cache.set('finder-location-subnotberkeley-%s' % snbkey, subnotberkeley, FORM_CACHE_TIME)
					for j in subnotberkeley:
						if j.display_name != '':
							name = '%s, %s' % (j.display_name, j.address)
						else:
							name = '%s' % (j.address)
						if j in options:
							choices.append((j.pk, mark_safe('<span id="form-location-val-%s">%s</span>' % (j.pk, name)), False))
						else:
							choices.append((j.pk, mark_safe('<span style="color: #888;" id="form-location-val-%s">%s</span>' % (j.pk, name)), True))
				else:
					choices.append(((None, i['city'].replace(' ', '_')), mark_safe('<span style="color: #888;" id="form-location-val-%s">%s</span>' % (i['city'].replace(' ', '_'), i['city'])), True))
			self.fields['location'].choices = choices
			if initial:
				cache.set('finder-locations', choices, FORM_CACHE_TIME)
		else:
			self.fields['location'].choices = choices

		choices = None
		if initial:
			choices = cache.get('finder-specialty')
		if not choices:
			choices = []
			options = set()
			ls = cache.get('finder-doctor-specialty')
			if ls:
				for d in specialty_filter:
					options.add(d.title_service)
					for s in ls[d]:
						options.add(s)
			else:
				ls = dict()
				for d in specialty_filter:
					ls[d] = []
					options.add(d.title_service)
					dservices = cache.get('finder-doctor-services-%s' % d.id)
					if not dservices:
						dservices = list(d.services.all())
						cache.set('finder-doctor-services-%s' % d.id, dservices, FORM_CACHE_TIME)
					for s in dservices:
						options.add(s)
						ls[d].append(s)
				if initial:
					cache.set('finder-doctor-specialty', ls, FORM_CACHE_TIME)
			services = cache.get('finder-services-list')
			if not services:
				services = list(Service.objects.order_by('name'))
				cache.set('finder-services-list', services, FORM_CACHE_TIME)
			for i in services:
				if i in options:
					choices.append((i.pk, mark_safe('<span id="form-specialty-val-%d">%s</span>' % (i.pk, unicode(i))), False))
				else:
					choices.append((i.pk, mark_safe('<span style="color: #888;" id="form-specialty-val-%d">%s</span>' % (i.pk, unicode(i))), True))
			self.fields['specialty'].choices = choices
			if initial:
				cache.set('finder-specialty', choices, FORM_CACHE_TIME)
		else:
			self.fields['specialty'].choices = choices

		choices = None
		if initial:
			choices = cache.get('finder-gender')
		if not choices:
			choices = []
			options = set()
			for d in gender_filter:
				options.add(d.gender)
			for i in Doctor.GENDER:
				if i[0] in options:
					choices.append((i[0], mark_safe('<span id="form-gender-val-%s">%s</span>' % (i[0], i[1])), False))
				else:
					choices.append((i[0], mark_safe('<span style="color: #888;" id="form-gender-val-%s">%s</span>' % (i[0], i[1])), True))
			self.fields['gender'].choices = choices
			if initial:
				cache.set('finder-gender', choices, FORM_CACHE_TIME)
		else:
			self.fields['gender'].choices = choices

		choices = None
		if initial:
			choices = cache.get('finder-hospitals')
		if not choices:
			choices = []
			options = set()
			ls = cache.get('finder-doctor-hospitals')
			if ls:
				for d in hospitals_filter:
					for h in ls[d]:
						options.add(h)
			else:
				ls = dict()
				for d in hospitals_filter:
					ls[d] = []
					dhospitals = cache.get('finder-doctor-hospitals-%s' % d.id)
					if not dhospitals:
						dhospitals = list(d.hospitals.all())
						cache.set('finder-doctor-hospitals-%s' % d.id, dhospitals, FORM_CACHE_TIME)
					for h in dhospitals:
						options.add(h)
						ls[d].append(h)
				if initial:
					cache.set('finder-doctor-hospitals', ls, FORM_CACHE_TIME)
			hospitals = cache.get('finder-hospitals-list')
			if not hospitals:
				hospitals = list(Hospital.objects.order_by('hospital'))
				cache.set('finder-hospitals-list', hospitals, FORM_CACHE_TIME)
			for i in hospitals:
				if i in options:
					choices.append((i.pk, mark_safe('<span id="form-hospitals-val-%d">%s</span>' % (i.pk, unicode(i))), False))
				else:
					choices.append((i.pk, mark_safe('<span style="color: #888;" id="form-hospitals-val-%d">%s</span>' % (i.pk, unicode(i))), True))
			self.fields['hospitals'].choices = choices
			if initial:
				cache.set('finder-hospitals', choices, FORM_CACHE_TIME)
		else:
			self.fields['hospitals'].choices = choices

		choices = None
		if initial:
			choices = cache.get('finder-languages')
		if not choices:
			choices = []
			options = set()
			ls = cache.get('finder-doctor-languages')
			if ls:
				for d in languages_filter:
					for l in ls[d]:
						options.add(l)
			else:
				ls = dict()
				for d in languages_filter:
					ls[d] = []
					for l in d.languages.all():
						options.add(l)
						ls[d].append(l)
				if initial:
					cache.set('finder-doctor-languages', ls, FORM_CACHE_TIME)
			languages = cache.get('finder-languages-list')
			if not languages:
				languages = list(Language.objects.order_by('language'))
				cache.set('finder-languages-list', languages, FORM_CACHE_TIME)
			for i in languages:
				if i in options:
					choices.append((i.pk, mark_safe('<span id="form-languages-val-%d">%s</span>' % (i.pk, unicode(i))), False))
				else:
					choices.append((i.pk, mark_safe('<span style="color: #888;" id="form-languages-val-%d">%s</span>' % (i.pk, unicode(i))), True))
			self.fields['languages'].choices = choices
			if initial:
				cache.set('finder-languages', choices, FORM_CACHE_TIME)
		else:
			self.fields['languages'].choices = choices

	location = DoctorFinderChoiceField(required=False, widget=DoctorFinderChoiceWidget())
	specialty = DoctorFinderChoiceField(required=False, widget=DoctorFinderChoiceWidget())
	gender = DoctorFinderChoiceField(required=False, widget=DoctorFinderChoiceWidget())
	hospitals = DoctorFinderChoiceField(required=False, widget=DoctorFinderChoiceWidget())
	languages = DoctorFinderChoiceField(required=False, widget=DoctorFinderChoiceWidget())

# TODO - can this be removed?
@cache_page(CACHE_TIME)
def doctor_finder(request):
	doctors = cache.get('finder-doctors-all')
	if not doctors:
		doctors = Doctor.objects.order_by('last_name', 'first_name').exclude(exclude_from_index=cms.EXCLUDE)
		cache.set('finder-doctors-all', doctors, FORM_CACHE_TIME)
	keystr = ''
	for (key, vallist) in request.POST.lists():
		for (val) in vallist:
			if key != 'ajax' and key != 'counter':
				keystr += '%s:%s,' % (key, val)
	form = None
	if keystr == '':
		keystr = 'master'
	else:
		keystr = quote_plus(keystr)
	print "KEYSTR====", keystr
	form = cache.get('finder-processed-form-%s' % keystr)
	if not form:
		form = DoctorFinderForm(request.REQUEST)
	form.set_choices(True, doctors)
	if form.is_valid():
		location_filter = doctors
		specialty_filter = doctors
		gender_filter = doctors
		hospitals_filter = doctors
		languages_filter = doctors
		if form.cleaned_data['location']:
			cities = []
			locations = []
			for location in form.cleaned_data['location']:
				if location[0] == '(':
					cities.append(location[9:].replace('_', ' ').replace("')", ''))
				else:
					locations.append(location)
			if cities:
				doctors = doctors.filter(location__location__city__in=cities)
			if locations:
				doctors = doctors.filter(location__location__in=locations)
			specialty_filter = doctors
			gender_filter = doctors
			hospitals_filter = doctors
			languages_filter = doctors
		specialty = False
		if form.cleaned_data['specialty']:
			specialty = True
			doctors = doctors.filter(Q(title_service__in=form.cleaned_data['specialty']) | Q(services__in=form.cleaned_data['specialty']))
			location_filter = doctors
			gender_filter = doctors
			hospitals_filter = doctors
			languages_filter = doctors
		gender = False
		if form.cleaned_data['gender']:
			gender = True
			doctors = doctors.filter(gender__in=form.cleaned_data['gender'])
			if specialty:
				specialty_filter = specialty_filter.filter(gender__in=form.cleaned_data['gender'])
			else:
				specialty_filter = doctors
			location_filter = doctors
			hospitals_filter = doctors
			languages_filter = doctors
		hospitals = False
		if form.cleaned_data['hospitals']:
			hospitals = True
			doctors = doctors.filter(hospitals__in=form.cleaned_data['hospitals'])
			if gender:
				gender_filter = gender_filter.filter(hospitals__in=form.cleaned_data['hospitals'])
			else:
				gender_filter = doctors
			if specialty:
				specialty_filter = specialty_filter.filter(hospitals__in=form.cleaned_data['hospitals'])
			else:
				specialty_filter = doctors
			location_filter = doctors
			languages_filter = languages_filter.filter(hospitals__in=form.cleaned_data['hospitals'])
		if form.cleaned_data['languages']:
			doctors = doctors.filter(languages__in=form.cleaned_data['languages'])
			if hospitals:
				hospitals_filter = hospitals_filter.filter(languages__in=form.cleaned_data['languages'])
			else:
				hospitals_filter = doctors
			if gender:
				gender_filter = gender_filter.filter(hospitals__in=form.cleaned_data['hospitals'])
			else:
				gender_filter = doctors
			if specialty:
				specialty_filter = specialty_filter.filter(hospitals__in=form.cleaned_data['hospitals'])
			else:
				specialty_filter = doctors
			location_filter = doctors
		doctors = doctors.distinct()
		form.set_choices(False, doctors, location_filter, specialty_filter, gender_filter, languages_filter, hospitals_filter)
		cache.set('finder-processed-form-%s' % keystr, form, FORM_CACHE_TIME)
	# List by letter
	pos = 0
	letters = []
	while pos < len(doctors):
		letter = doctors[pos].letter_key()
		x = pos
		while x < len(doctors) and letter == doctors[x].letter_key():
			x += 1
		count = x - pos
		offset = 0
		rows = []
		row = []
		for doctor in doctors[pos:pos+count]:
			if offset == 3:
				rows.append(row)
				row = []
				offset = 0
			row.append(doctor)
			offset += 1
		rows.append(row)
		letters.append(RowList(letter, rows))
		pos = pos + count
	template = 'doctors/doctor-finder.html'
	if 'ajax' in request.REQUEST and request.REQUEST['ajax'] == 'True':
		t = loader.get_template('doctors/doctor-finder-results.json')
		c = RequestContext(request, {'doctors': doctors, 'letters': letters, 'form': form, 'counter': request.REQUEST.get('counter')})
		return HttpResponse(t.render(c), mimetype='application/javascript')
	return render_to_response(template, {'doctors': doctors, 'letters': letters, 'form': form}, context_instance=RequestContext(request))




"""
Doctor bulk import form for the doctor-finder application.

This is a temporary form to gather new doctor data for
the December 2010 enhancement launch.
"""

class DoctorDataForm(forms.Form):
	pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
	name = forms.CharField(required=False)
	gender = forms.ChoiceField(required=False, choices=([("", "Select Gender")] + [gender for gender in Doctor.GENDER]))
	hospitals = forms.ModelMultipleChoiceField(required=False, queryset=Hospital.objects.all())
	accepting = forms.ChoiceField(required=False, choices=([("", "Accepting new patients?")] + [accepting for accepting in Doctor.ACCEPTING]))
	languages = forms.ModelMultipleChoiceField(required=False, queryset=Language.objects.all())

@login_required
def bulk_entry(request):
	if request.method == 'POST':
		ArticleFormSet = formset_factory(DoctorDataForm, extra=0)
		formset = ArticleFormSet(request.POST)
		if formset.is_valid():
			for form in formset.forms:
				try:
					changes = False
					doctor = Doctor.all_objects.get(pk=form.cleaned_data['pk'])
					if set(form.cleaned_data['languages']) ^ set([l for l in doctor.languages.all()]):
						doctor.languages.clear()
						for language in form.cleaned_data['languages']:
							doctor.languages.add(language)
						changes = True
					if set(form.cleaned_data['hospitals']) ^ set([l for l in doctor.hospitals.all()]):
						doctor.hospitals.clear()
						for hospital in form.cleaned_data['hospitals']:
							doctor.hospitals.add(hospital)
						changes = True
					if doctor.gender != form.cleaned_data['gender']:
						doctor.gender = form.cleaned_data['gender']
						changes = True
					if doctor.accepting != form.cleaned_data['accepting']:
						doctor.accepting = form.cleaned_data['accepting']
						changes = True
					if changes:
						doctor.save(preview=False)
				except Doctor.DoesNotExist:
					pass
			return render_to_response('admin/doctors/bulk-input.html', {'formset': formset}, context_instance=RequestContext(request))
		else:
			return render_to_response('admin/doctors/bulk-input.html', {'formset': formset}, context_instance=RequestContext(request))
	else:
		ArticleFormSet = formset_factory(DoctorDataForm, extra=0)
		formset = ArticleFormSet(initial=[{'pk': d.pk, 'name': d.list_name, 'gender': d.gender, 'hospitals': d.hospitals.all(), 'accepting': d.accepting, 'languages': d.languages.all()} for d in Doctor.all_objects.order_by('last_name', 'first_name')])
		return render_to_response('admin/doctors/bulk-input.html', {'formset': formset}, context_instance=RequestContext(request))


@login_required
def admin_accepting(request):
	doctors = Doctor.objects.all().order_by('last_name', 'first_name')
	return render_to_response('admin/doctors/doctor/accepting.html', {'error': None, 'doctors': doctors, 'accepting_options': Doctor.ACCEPTING}, context_instance=RequestContext(request))

@login_required
def admin_set_accepting(request):
	if request.method == 'POST':
		flag_changes = dict()
		text_changes = dict()
		for v in request.POST.iterlists():
			if v[0].startswith('accepting_flag'):
				flag_changes[int(v[0][v[0].rindex('_')+1:])] = v[1][0]
			if v[0].startswith('accepting_text') and v[1][0] != '':
				text_changes[int(v[0][v[0].rindex('_')+1:])] = v[1][0]
		for d in Doctor.objects.all():
			change = False
			if flag_changes.has_key(d.id) and d.accepting_flag != flag_changes[d.id]:
				change = True
				d.accepting_flag = flag_changes[d.id]
			if text_changes.has_key(d.id) and d.accepting != text_changes[d.id]:
				change = True
				d.accepting = text_changes[d.id]
			if change:
				d.save(preview=False)
	return HttpResponseRedirect('/admin/doctors/doctor/accepting/')


def doctor_specialty(request):
	"""
	Return results for a specialty search.
	"""
	try:
		query = request.REQUEST['search-input']
	except KeyError:
		query = ''
	(count, results) = interface.search(0, 'complete', 'doctors.Specialty', 'score', query, query)
	doctors = []
	for result in results:
		try:
			for doctor in Doctor.objects.filter(specialties=result.key):
				doctors.append(doctor)
		except ValueError:
			# This is probably a Keyword result to be ignored
			pass
	set = {}
	map(set.__setitem__, doctors, [])
	doctors = set.keys()
	doctors.sort(key=lambda x: x.last_name)
	return render_to_response('doctors/specialty.html', {'query': query, 'count': len(doctors), 'doctors': doctors}, context_instance=RequestContext(request))


def doctor_survey_index(request):
	"""
	Return an initial sub-specialty form to select a doctor.
	"""
	doctors = Doctor.objects.all()
	return render_to_response('doctors/specialty_select.html', {'doctors': doctors})

def doctor_survey(request):
	doctor_id = request.REQUEST['doctor']
	doctor = Doctor.objects.get(id=doctor_id)

	return render_to_response('doctors/specialty_edit.html', {'doctor': doctor, 'range': range(20)})

def doctor_survey_submit(request):
	doctor_id = request.REQUEST['doctor']
	doctor = Doctor.objects.get(id=doctor_id)
	for k, v in request.REQUEST.items():
		if k.find('specialty-') == 0 and v:
			vs = re.sub(r'["\']+', '', v)
			u = SpecialtyUpdate(doctor=doctor, specialty=vs)
			u.save()

	return render_to_response('doctors/specialty_done.html', {'doctor': doctor})

@login_required
def specialty_export(request):
	doctors = []
	for d in Doctor.objects.all().order_by('last_name', 'first_name'):
		if len(d.specialtyupdate_set.all()) > 0:
			doctors.append(d)
	return render_to_response('admin/doctors/specialty_export.html', {'doctors': doctors}, mimetype='application/ms-excel')

@login_required
def no_specialty_export(request):
	doctors = []
	for d in Doctor.objects.all().order_by('last_name', 'first_name'):
		if len(d.specialties.all()) == 0:
			doctors.append(d)
	return render_to_response('admin/doctors/no_specialty_export.html', {'doctors': doctors}, mimetype='application/ms-excel')
