from datetime import datetime
import re
import json
from random import randint
import string

from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django import forms

from smgsite.settings import CACHE_TIME, TEMPLATE_ROOT, MEDIA_URL
from smgsite.services.models import Service
from smgsite.site.models import Location, VideoTemplate, UnsubscribeChoices, Unsubscribe
from smgsite.pages.models import Template, Directory, Page
from smgsite.search.interface import title_re
import smgsite.healthday.models as healthday
import smgsite.articles.models as articles
from smgsite.doctors.forms import DoctorFinderForm, ConditionFinderForm
from smgsite.site.forms import CitySelectForm

zip_re = re.compile(r'\d\d\d\d\d(-\d\d\d\d){0,1}')


class City(object):
	def __init__(self, name, location):
		self.name = name
		self.locations = [location]
        
def mainvideo(request):
	"""
	This view returns jsonp data so we can inject a video on the mobile site.
	"""
	json_result = {'success':'false'}
	if request.method == "GET":
		templates = VideoTemplate.objects.filter(location='H')
		template = templates[randint(0, len(templates)-1)]
		json_result = json.dumps({'video': template.template, 'description': template.description})
            
		if request.GET.has_key(u'callback'):
			json_result = "%s(%s)" % (request.GET[u'callback'],json_result)
    
	return HttpResponse(json_result, mimetype='application/json')
	
def slider(request):
	"""
	This view returns jsonp data so we can inject a slider on the mobile site.
	"""
	json_result = {'success':'False'}
	if request.method == "GET":
		data = articles.Article.objects.filter(leader_promo__gt=0).order_by('leader_promo')
		html_slider = loader.render_to_string('helpers/_slider.html', {'slides':data})
            
		json_result = json.dumps({'slider': html_slider})
            
		if request.GET.has_key(u'callback'):
			json_result = "%s(%s)" % (request.GET[u'callback'],json_result)
    
	return HttpResponse(json_result, mimetype='application/json')

def dynamic(request):
	"""
	Sets dynamic flags for printer friendly and small device views.
	"""
	#print request
	printable = False
	if request.GET.get('printable'):
		printable = True
	blackberry = False
	if request.META.get('HTTP_USER_AGENT') and request.META['HTTP_USER_AGENT'].startswith('BlackBerry'):
		blackberry = True
	return {'printable': printable, 'blackberry': blackberry}

@cache_page(CACHE_TIME)
def dynamic_css(request, template):
	"""
	Return a dynamically rendered CSS template.
	"""
        t = loader.get_template('css/%s' % template)
        c = RequestContext(request)
        return HttpResponse(t.render(c), mimetype='text/css')

def index(request):
	"""
	This renders the homepage
	"""
	last_updated = datetime.now()
	results = healthday.Article.objects.order_by('-posting_time')[:1]
	try:
		last_updated = results[0].posting_time
	except IndexError:
		pass
	doctor_finder_form = DoctorFinderForm()
	condition_finder_form = ConditionFinderForm()
	ctx = {
		'last_updated': last_updated,
		'doctor_finder_form': doctor_finder_form,
		'condition_finder_form': condition_finder_form,
	}
	return render_to_response('index.html', ctx, context_instance=RequestContext(request))

def index_test(request):
	"""
	This renders the homepage
	"""
	last_updated = datetime.now()
	results = healthday.Article.objects.order_by('-posting_time')[:1]
	try:
		last_updated = results[0].posting_time
	except IndexError:
		pass
	return render_to_response('little.html', {'last_updated': last_updated}, context_instance=RequestContext(request))

def about_page(request, path):
	"""
	This renders the subservice display page.
	"""
	path = 'about/%s' % (path)
	path = path.strip('/').split('/')
	pathdir = '/'.join(path[0:-1])
	pathfile = path[-1]
	print "Pathdir is %s" % pathdir
	print "Pathfile is %s" % pathfile
	try:
		if request.user.is_authenticated():
			directory = Directory.objects.get(directory=pathdir)
		else:
			directory = Directory.objects.get(directory=pathdir)
	except Directory.DoesNotExist:
		raise Http404
	try:
		if request.user.is_authenticated():
			page = Page.qa_objects.get(directory=directory, urlname=pathfile)
		else:
			page = Page.objects.get(directory=directory, urlname=pathfile)
	except Page.DoesNotExist:
		raise Http404
	template = 'pages/%s' % directory.template.name
	media_re = re.compile(r'(<img[^>]+src=\")/media')
	content = media_re.sub('\\1%s' % MEDIA_URL, page.content)
	return render_to_response(template, {'page': page, 'content': content}, context_instance=RequestContext(request))

def about_index(request):
		"""
		This delivers the top level About section page
		"""
		return about_page(request, 'index.html')
		#return render_to_response('site/about.html', {}, context_instance=RequestContext(request))

#TODO: remove??
def locations_old(request):
	"""
	This renders the locations page.

	Updated 8/16/11 to group by city
	"""
	if request.user.is_authenticated():
		locations = Location.qa_objects.filter(display=Location.SHOW).order_by('order')
	else:
		locations = Location.objects.filter(display=Location.SHOW).order_by('order')
	cities = dict()
	for location in locations:
		if location.city in cities:
			cities[location.city].locations.append(location)
		else:
			cities[location.city] = City(location.city, location)
	berkeley = cities.pop('Berkeley Heights')
	cities = sorted(cities.values(), key=lambda c: c.name)
	cities.insert(0, berkeley)
	try:
		if request.user.is_authenticated():
			directory = Directory.objects.get(directory='locations')
		else:
			directory = Directory.objects.get(directory='locations')
		if request.user.is_authenticated():
			page = Page.qa_objects.get(directory=directory, urlname='transportation')
		else:
			page = Page.objects.get(directory=directory, urlname='transportation')
		media_re = re.compile(r'(<img[^>]+src=\")/media')
		content = media_re.sub('\\1%s' % MEDIA_URL, page.content)
	except (Page.DoesNotExist, Directory.DoesNotExist):
		content = ''
        """
        Updated 2/19/11 to write a new JSON object for maps
        """
        mlocations = list()
        for location in locations:
                mlocation = {
                        'name': location.name,
                        'address': location.address,
                        'lat': float(location.glatitude),
                        'lng': float(location.glongitude),
                        'image': location.image.url,
                        'url': location.get_absolute_url(),
                }
                mlocations.append(mlocation)
        mlocstr = json.dumps(mlocations)
        return render_to_response('site/locations.html', {'cities': cities, 'locations': locations, 'transportation': content, 'smg_locations': mlocstr}, context_instance=RequestContext(request))



def locations(request):
	"""
	New locations view 2014 locations grouped by city with a form to change it.
	"""
	location_form = CitySelectForm(request.GET)
	city = request.GET.get('city', None)
	locations = Location.objects.filter(display=Location.SHOW, city=city)
	if locations.count() == 0:
		city = None
	"""
	if not city or locations.count() == 0:
		# redirect to default city berkeley heights
		return HttpResponseRedirect('/locations/?city=Berkeley+Heights')
	"""
	mlocations = list()
	#for location in locations:
	for index, location in enumerate(locations):
		alpha = string.uppercase[index]
		mlocation = {
			'name': location.get_display_name,
			'address': location.display_address,
			'lat': float(location.glatitude),
			'lng': float(location.glongitude),
			#'image': location.image.url,
			'url': location.get_absolute_url(),
			'marker': 'http://maps.google.com/mapfiles/marker%s.png' % alpha,
		}
		mlocations.append(mlocation)

	ctx = {
		'location_form': location_form,
		'locations': locations,
		'city': city,
		'smg_locations': json.dumps(mlocations),
	}
	return render(request, 'site/locations.html', ctx)



def locations_redirect(request):
	return HttpResponseRedirect('/locations/')

#TODO: Remove?
def location_hours_popup(request, location):
	"""
	This renders the location hours popup detail page.
	"""
	try:
		if request.user.is_authenticated():
			location = Location.qa_objects.get(pk=location)
		else:
			location = Location.objects.get(pk=location)
	except Location.DoesNotExist:
		raise Http404
	weekday = location.weekdayhours_set.all().order_by('position')
	saturday = location.saturdayhours_set.all().order_by('position')
	sunday = location.sundayhours_set.all().order_by('position')
	return render_to_response('site/location_hours_popup.html', {'location':location, 'weekday': weekday, 'saturday': saturday, 'sunday': sunday}, context_instance=RequestContext(request))

def location(request, location):
	"""
	This renders the location detail page.
	"""
	try:
		if request.user.is_authenticated():
			location = Location.qa_objects.get(urlname=location)
		else:
			location = Location.objects.get(urlname=location)
	except Location.DoesNotExist:
		raise Http404

	doctors = [y.doctor for y in location.doctors_location.filter(active=u'1') if y.doctor.active == u'1']
	doctors = sorted(doctors, key = lambda x: x.last_name)
	services = [y.service for y in location.services_location.filter(active=u'1') if y.service.active == u'1']
	services = sorted(services, key = lambda x: x.name)
	
	weekday = location.weekdayhours_set.all().order_by('position')
	saturday = location.saturdayhours_set.all().order_by('position')
	sunday = location.sundayhours_set.all().order_by('position')

	ctx = {
		'location': location, 
		'doctors': doctors, 
		'services': services, 
		'weekday': weekday,
		'saturday': saturday,
		'sunday': sunday,
	}
	return render(request, 'site/location.html', ctx)

def locations_all(request):
	locations = Location.objects.filter(display=Location.SHOW).order_by('city')

	mlocations = list()
	#for location in locations:
	for index, location in enumerate(locations):
		# more than 26 so no good using alpha markers here
		#alpha = string.uppercase[index]
		mlocation = {
			'name': location.get_display_name,
			'address': location.display_address,
			'lat': float(location.glatitude),
			'lng': float(location.glongitude),
			#'image': location.image.url,
			'url': location.get_absolute_url(),
			'marker': 'http://maps.google.com/mapfiles/marker.png',
		}
		mlocations.append(mlocation)

	ctx = {
		'locations': locations,
		'smg_locations': json.dumps(mlocations),
		}


	return render(request, 'site/locations_all.html', ctx)


promotion_urls = {
'news1': 'utm_source=starledger&utm_medium=newspaper&utm_campaign=brandlaunch',
'news2': 'utm_source=independent&utm_medium=newspaper&utm_campaign=brandlaunch',
'news3': 'utm_source=independent-ins&utm_medium=newspaper&utm_campaign=brandlaunch',
'news4': 'utm_source=vicinity&utm_medium=magazine&utm_campaign=brandlaunch',
'news5': 'utm_source=connection&utm_medium=magazine&utm_campaign=brandlaunch',
'news6': 'utm_source=hometownq&utm_medium=magazine&utm_campaign=brandlaunch',
'news7': 'utm_source=collection&utm_medium=magazine&utm_campaign=brandlaunch',
'news8': 'utm_source=MNI&utm_medium=magazine&utm_campaign=brandlaunch',
'news9': 'utm_source=njmonthly&utm_medium=magazine&utm_campaign=brandlaunch',
'news10': 'utm_source=un-mo-family&utm_medium=magazine&utm_campaign=brandlaunch',
'news11': 'utm_source=papermill&utm_medium=program&utm_campaign=brandlaunch',
}
def promotion(request, number):
	"""
	This is a pageless tracking point for external promotions.
	"""
	key = 'news%s' % number
	redirect = '/'
	if promotion_urls.has_key(key):
		redirect = '/?%s' % promotion_urls[key]
	return HttpResponseRedirect(redirect)


class EmailForm(forms.Form):
	title = forms.CharField(widget=forms.HiddenInput)
	referrer = forms.CharField(widget=forms.HiddenInput)
	s_name = forms.CharField(widget=forms.TextInput(attrs={'size':'35'}))
	s_email = forms.EmailField(widget=forms.TextInput(attrs={'size':'35'}))
	r_name = forms.CharField(widget=forms.TextInput(attrs={'size':'35'}))
	r_email = forms.EmailField(widget=forms.TextInput(attrs={'size':'35'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'cols':'35','rows':'5'}))


def email_page(request):
	from django.core.mail import EmailMessage
	from urllib import quote, unquote
	import re
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			title = unquote(data['title'])
			link = unquote(data['referrer'])
			s_name = data['s_name']
			s_email = data['s_email']
			r_name = data['r_name']
			r_email = data['r_email']
			message = data['message']
			response = '%s,\n\n' % r_name
			if message:
				response = '%s%s\n\n' % (response, message)
			response = '%sI thought you\'d be interested in %s.\n\n%s\n\nIf you are unable to click the link, you can enter %s in your browser\'s address bar.\n\nYou can also go to Summit Medical Group\'s home page at http://www.summitmedicalgroup.com/.\n\nSincerely,\n%s' % (response, title, link, link, r_name)
			msg = EmailMessage(title, response, s_email, [r_email])
			msg.fail_silently = True
			msg.send()
			return render_to_response('site/sent_page_form.html', context_instance=RequestContext(request))
		else:
			empty_error = False
			email_error = False
			for e in form.errors.values():
				print "Error value --%s--" % e.as_text()
				if e.as_text() == '* This field is required.':
					empty_error = True
				if e.as_text() == '* Enter a valid e-mail address.':
					email_error = True
			return render_to_response('site/send_page_form.html', {'form': form, 'empty_error': empty_error, 'email_error': email_error}, context_instance=RequestContext(request))
	else:
		referrer_re = re.compile(r'referrer=([^&]+)')
		title_re = re.compile(r'title=([^&]+)')
		referrer = referrer_re.search(request.META['QUERY_STRING']).group(1)
		title = title_re.search(request.META['QUERY_STRING']).group(1)
		form = EmailForm(initial={'title': title, 'referrer': referrer})
		return render_to_response('site/send_page_form.html', {'form': form}, context_instance=RequestContext(request))


class UnsubscribeForm(forms.Form):


	STATES = (
		('CT', 'Connecticut'),
		('DE', 'Delaware'),
		('NJ', 'New Jersey'),
		('NY', 'New York'),
		('PA', 'Pennsylvania')
	)

	REASONS = (
		(2, 'Do not remember subscribing'),
		(3, 'No longer a patient'),
		(4, 'Receive too much mail'),
	)

	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	street_1 = forms.CharField(max_length=200)
	street_2 = forms.CharField(required=False, max_length=200)
	city = forms.CharField(max_length=100)
	state = forms.ChoiceField(choices=STATES, initial='NJ')
	zipcode = forms.CharField(max_length=10)
	email = forms.EmailField(required=False)
	reasons = forms.MultipleChoiceField(choices=REASONS, widget=forms.CheckboxSelectMultiple)
	def clean_zipcode(self):
		match = zip_re.match(self.cleaned_data['zipcode'])
		if not match:
			raise forms.ValidationError('Zip code is not in 5 digit or 5-4 digit format.')
		return self.cleaned_data['zipcode']


def unsubscribe(request):
	if request.method == 'POST':
		form = UnsubscribeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			u = Unsubscribe(first_name=data['first_name'], last_name=data['last_name'], street_1=data['street_1'], street_2=data['street_2'], city=data['city'], state=data['state'], zipcode=data['zipcode'], email=data['email'])
			u.save()
			for e in data['reasons']:
				v = UnsubscribeChoices.objects.get(pk=e)
				u.reasons.add(v)
			u.save()
			return render_to_response('site/unsubscribe/unsubscribed.html', context_instance=RequestContext(request))
		else:
			return render_to_response('site/unsubscribe/unsubscribe.html', {'form': form}, context_instance=RequestContext(request))
	else:
		form = UnsubscribeForm()
		return render_to_response('site/unsubscribe/unsubscribe.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def export_unsubscribe(request):
	unsubscribes = Unsubscribe.objects.all()
	return render_to_response('admin/site/unsubscribe/export_unsubscribes.html', {'unsubscribes': unsubscribes}, context_instance=RequestContext(request), mimetype='application/ms-excel')

