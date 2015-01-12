import md5
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.util import ErrorList
from smgsite.mysmg.models import User, UserProfile, Link
from smgsite.services.models import Service
from smgsite.doctors.models import Doctor

def home(request):
	"""
	Homepage for MySMG -- now without the library.
	"""
	user = None
	authenticated = request.session.get('authenticated')					
	if authenticated:
		user = User.objects.get(username=request.session['username'])
	return render_to_response('mysmg/home.html', {'authenticated': authenticated, 'user': user}, context_instance=RequestContext(request))

def view(request, added="None", item="None"):
	"""
	Primary method to view MySMG resources.
	"""
	authenticated = request.session.get('authenticated')					
	if authenticated:
		user = User.objects.get(username=request.session['username'])
		profile = user.userprofile_set.get()
		if request.GET.get('action'):
			try:
				if request.GET['action'] == 'remove':
					model = request.GET.get('type')
					pk = request.GET.get('pk')
					url = request.GET.get('url')
					if model == 'doctor':
						profile.my_doctors.remove(profile.my_doctors.filter(pk=pk)[0])
					elif model == 'service':
						profile.my_services.remove(profile.my_services.filter(pk=pk)[0])
					elif model == 'library':
						profile.my_library.remove(profile.my_library.filter(url=url)[0])
			except:
				pass
		services = [service for service in profile.my_services.all()]
		doctors = [doctor for doctor in profile.my_doctors.all()]
		library = [(link.url, link.title) for link in profile.my_library.all()]
		return render_to_response('mysmg/my_library.html', {'authenticated': True, 'user': user, 'services': services, 'doctors': doctors, 'library': library, 'added': added, 'item': item}, context_instance=RequestContext(request))
	else:
		if request.GET.get('action'):
			try:
				if request.GET['action'] == 'remove':
					model = request.GET.get('type')
					pk = request.GET.get('pk')
					url = request.GET.get('url')
					if model == 'doctor':
						request.session['my_doctors'].remove(pk)
						request.session['my_doctors'] = request.session['my_doctors']
					elif model == 'service':
						request.session['my_services'].remove(pk)
						request.session['my_services'] = request.session['my_services']
					elif model == 'library':
						#print request.session['my_library']
						for entry in request.session['my_library']:
							if entry[0] == url:
								request.session['my_library'].remove(entry)
								request.session['my_library'] = request.session['my_library']
								break
			except:
				pass
		user = None
		services = []
		if request.session.get('my_services'):
			for pk in request.session['my_services']:
				try:
					services.append(Service.objects.get(pk=pk))
				except Service.DoesNotExist:
					print 'Service key error!'
		doctors = []
		if request.session.get('my_doctors'):
			for pk in request.session['my_doctors']:
				try:
					doctors.append(Doctor.objects.get(pk=pk))
				except Doctor.DoesNotExist:
					print 'Doctors key error!'
		library = []
		if request.session.get('my_library'):
			library = request.session['my_library']
		return render_to_response('mysmg/my_library.html', {'authenticated': False, 'user': None, 'services': services, 'doctors': doctors, 'library': library, 'added': added, 'item': item}, context_instance=RequestContext(request))

def add(request):
	from urlparse import urlparse
	"""
	Non-AJAX return method for handling MySMG page additions.
	"""
	added = 'None'
	item = 'None'
	if request.session.get('authenticated'):
		user = User.objects.get(username=request.session['username'])
		profile = user.userprofile_set.get()
		if request.GET.get('url'):
			url = urlparse(request.GET['url'])
			title = request.GET['title']
			for link in profile.my_library.all():
				if url[2] == link.url:
					return view(request, added='duplicate')
			link = Link(url=url[2], title=title)
			link.save()
			profile.my_library.add(link)
			added = 'Library'
			item = url[2]
		else:
			model = request.GET['model']
			pk = request.GET['pk']
			if model == 'service':
				for service in profile.my_services.all():
					if str(service.pk) == pk:
						return view(request, added='duplicate')
				service = Service.objects.get(pk=pk)
				profile.my_services.add(service)
				added = 'service'
				item = service.pk
			elif model == 'doctor':
				for doctor in profile.my_doctors.all():
					if str(doctor.pk) == pk:
						return view(request, added='duplicate')
				doctor = Doctor.objects.get(pk=pk)
				profile.my_doctors.add(doctor)
				added = 'doctor'
				item = doctor.pk
	else: # User is not authenticated
		if request.GET.get('url'):
			url = urlparse(request.GET['url'])
			title = request.GET['title']
			try:
				for link in request.session['my_library']:
					if url[2] == link[0]:
						return view(request, added='duplicate')
			except KeyError:
				pass
			try:
				request.session['my_library'] = request.session['my_library'] + [(url[2], title)]
			except KeyError:
				request.session['my_library'] = [(url[2], title)]
			added = 'library'
			item = url[2]
		else:
			model = request.GET['model']
			pk = request.GET['pk']
			if model == 'service':
				try:
					for service in request.session['my_services']:
						if service == pk:
							return view(request, added='duplicate')
				except KeyError:
					pass
				try:
					request.session['my_services'] = request.session['my_services'] + [pk]
				except KeyError:
					request.session['my_services'] = [pk]
				added = 'service'
				item = pk
			elif model == 'doctor':
				try:
					for doctor in request.session['my_doctors']:
						if doctor == pk:
							return view(request, added='duplicate')
				except KeyError:
					pass
				try:
					request.session['my_doctors'] = request.session['my_doctors'] + [pk]
				except KeyError:
					request.session['my_doctors'] = [pk]
				added = 'doctor'
				item = pk
	return view(request, added=added, item=item)

def page(request, action):
	from urlparse import urlparse
	"""
	AJAX return method for handling MySMG page additions.
	"""
	if action == 'add':
		if request.session.get('authenticated'):
			user = User.objects.get(username=request.session['username'])
			profile = user.userprofile_set.get()
			if request.GET.get('url'):
				url = urlparse(request.GET['url'])
				title = request.GET['title']
				for link in profile.my_library.all():
					if url[2] == link.url:
						return render_to_response('mysmg/page.json', {'result': 'duplicate'})
				link = Link(url=url[2], title=title)
				link.save()
				profile.my_library.add(link)
			else:
				model = request.GET['model']
				pk = request.GET['pk']
				if model == 'service':
					for service in profile.my_services.all():
						if str(service.pk) == pk:
							return render_to_response('mysmg/page.json', {'result': 'duplicate'})
					service = Service.objects.get(pk=pk)
					profile.my_services.add(service)
				elif model == 'doctor':
					for doctor in profile.my_doctors.all():
						if str(doctor.pk) == pk:
							return render_to_response('mysmg/page.json', {'result': 'duplicate'})
					doctor = Doctor.objects.get(pk=pk)
					profile.my_doctors.add(doctor)
		else: # User is not authenticated
			if request.GET.get('url'):
				url = urlparse(request.GET['url'])
				title = request.GET['title']
				try:
					for link in request.session['my_library']:
						if url[2] == link[0]:
							return render_to_response('mysmg/page.json', {'result': 'duplicate'})
				except KeyError:
					pass
				try:
					request.session['my_library'] = request.session['my_library'] + [(url[2], title)]
				except KeyError:
					request.session['my_library'] = [(url[2], title)]
				#print request.session['my_library']
			else:
				model = request.GET['model']
				pk = request.GET['pk']
				if model == 'service':
					try:
						for service in request.session['my_services']:
							if service == pk:
								return render_to_response('mysmg/page.json', {'result': 'duplicate'})
					except KeyError:
						pass
					try:
						request.session['my_services'] = request.session['my_services'] + [pk]
					except KeyError:
						request.session['my_services'] = [pk]
				elif model == 'doctor':
					try:
						for doctor in request.session['my_doctors']:
							if doctor == pk:
								return render_to_response('mysmg/page.json', {'result': 'duplicate'})
					except KeyError:
						pass
					try:
						request.session['my_doctors'] = request.session['my_doctors'] + [pk]
					except KeyError:
						request.session['my_doctors'] = [pk]
	t = loader.get_template('mysmg/page.json')
	c = Context ({'result': 'okay'})
	r = HttpResponse(t.render(c))
	r.set_cookie('ajax_fancy', 'set_cookie!')
	return r

"""
User Registration Classes and Methods
"""

class RegisterForm(forms.Form):
	import re
	zip_re = re.compile(r'\d\d\d\d\d(-\d\d\d\d){0,1}')
	username = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class':'inp'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inp'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inp'}))
	
	first_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	middle_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	last_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	phone_area = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_phone_exchange"));'}))
	phone_exchange = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_phone_number"));'}))
	phone_number = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={'class':'inp', 'size':'4'}))
	phone = forms.CharField(required=False, widget=forms.HiddenInput())
	zipcode = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class':'inp inp_short'}))
	
	security_question = forms.ChoiceField(required=False, widget=forms.Select(attrs={'style':'width: 175px;'}), choices=(("", "Select one"), ("What is your mother's maiden name?", "Mother's Maiden Name"), ("What is your favorite pet's name?", "Favorite Pet's Name"), ("What is your town/city of birth?", "Birthplace (City/Town)")))
	security_answer = forms.CharField(max_length=50, required=False)
	
	contact = forms.ChoiceField(initial=False, choices=((True, "Yes, I'd like to subscribe."), (False, "No, thank you.")), widget=forms.RadioSelect(attrs={'class':'radio_buttons'}))
	def clean_username(self):
		try:
			user = User.objects.get(username=self.cleaned_data['username'])
			raise forms.ValidationError('username')
		except User.DoesNotExist:
			return self.cleaned_data['username']
	def clean_phone(self):
		phonestr = '(%s)-%s-%s' % (self.cleaned_data.get('phone_area'), self.cleaned_data.get('phone_exchange'), self.cleaned_data.get('phone_number'))
		return phonestr
	def clean_zipcode(self):
		zipcode = self.cleaned_data.get('zipcode')
		if zipcode:
			match = self.zip_re.match(zipcode)
			if not match:
				raise forms.ValidationError('zipcode')
		return zipcode
	def clean(self):
		if not self.cleaned_data.get('password'):
			raise forms.ValidationError('password')
		if not self.cleaned_data.get('password2'):
			raise forms.ValidationError('password2')
		p1 = self.cleaned_data['password']
		p2 = self.cleaned_data['password2']
		if len(p1) < 6 or len(p1) > 20:
			self._errors["password2"] = ErrorList(['password2'])
			raise forms.ValidationError('password2')
		if p1 != p2:
			self._errors["password2"] = ErrorList(['password2'])
			raise forms.ValidationError('password2')
		return self.cleaned_data

def register(request):
	import random
	from django.core.mail import EmailMessage
	from urllib import quote, unquote
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			confkey = '%d%d%d-%c%c' % (random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), chr(random.randrange(65, 91)), chr(random.randrange(65, 91)))
			data = form.cleaned_data
			user = User(active=False, username=data['username'], password=md5.new(data['password']).hexdigest(), first_name=data['first_name'], middle_name=data['middle_name'], last_name=data['last_name'], phone=data['phone'], zipcode=data['zipcode'], security_question=data['security_question'], security_answer=data['security_answer'], contact=data['contact'], confkey=confkey)
			user.save()
			profile = UserProfile(user=user)
			profile.save()
			if request.session.get('my_services'):
				for pk in request.session['my_services']:
					try:
						service = Service.objects.get(pk=pk)
						profile.my_services.add(service)
					except Service.DoesNotExist:
						pass
			if request.session.get('my_doctors'):
				for pk in request.session['my_doctors']:
					try:
						doctor = Doctor.objects.get(pk=pk)
						profile.my_doctors.add(doctor)
					except Doctor.DoesNotExist:
						pass
			if request.session.get('my_library'):
				for link in request.session['my_library']:
					link = Link(url=link[0], title=link[1])
					link.save()
					profile.my_library.add(link)
			profile.save()
			if user.first_name:
				salutation = user.first_name
			else:
				salutation = user.username
			subject = 'Summit Medical Group Account Confirmation'
			message = "Dear %s,\n\nThank you for registering for My Summit Medical Group--a personalized guide for you and your family's healthcare needs. As you use the site, you can save doctors, services, and information to view wherever you have access to the Internet. To get started, please click the link below to confirm your account.\n\nYou must confirm your account before beginning. You can consult the Help page for more information on how to save pages or use these tools.\n\nConfirm now by clicking:\nhttp://%s/mysummitmedicalgroup/register/confirm/?username=%s&confkey=%s\n\nIf the confirmation link does not work, please cut and paste the link into your browser's location/address bar.\n\nPlease note that this is Part I of your registration process. To email doctors, office staff and request lab or test results, you must also complete Part II of the registration, via the Communication tool link on the First Time Users page on MySummitMedical Group.\n\nHowever, not all Summit Medical Group physicians are participating in online communication. Click here to see if your doctor participates: http://www.summitmedicalgroup.com/about/My%%20Summit_Medical_Group_Doctors/\n\nSincerely,\n\nSummit Medical Group" % (salutation, request.META['HTTP_HOST'], data['username'], confkey)
			msg = EmailMessage(subject, message, 'register@summitmedicalgroup.com', [data['username']])
			msg.fail_silently = True
			msg.send()
			request.session.clear()
			return render_to_response('mysmg/register_confirm.html', {'user': user}, context_instance=RequestContext(request))
		else:
			return render_to_response('mysmg/register.html', {'form': form}, context_instance=RequestContext(request))
	else:
		form = RegisterForm()
		return render_to_response('mysmg/register.html', {'form': form}, context_instance=RequestContext(request))

class ConfirmationForm(forms.Form):
	"""
	Class for generating the user confirmation form
	"""
	username = forms.CharField(max_length=50)
	confkey = forms.CharField(max_length=6)
	def clean(self):
		try:
			username = self.cleaned_data['username']
		except KeyError:
			self._errors['username'] = ErrorList(['The e-mail address field is required.'])
			raise forms.ValidationError('username')
		try:
			confkey = self.cleaned_data['confkey']
		except KeyError:
			self._errors['confkey'] = ErrorList(['The confirmation key field is required.'])
			raise forms.ValidationError('confkey')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			self._errors['username'] = ErrorList(['Your e-mail address does not match any profiles in our system. Please verify that you have typed it correctly.'])
			raise forms.ValidationError('username')
		if user.active:
			self._errors['username'] = ErrorList(['The account for the e-mail address you have entered has already been confirmed. You may log in to your account using the <a href="/mysummitmedicalgroup/login/">login page</a>. If you have forgotten your password, you can also <a href="/mysummitmedicalgroup/forgot/">request a new password</a>.'])
			raise forms.ValidationError('username')
		if confkey != user.confkey:
			self._errors['confkey'] = ErrorList(['The confirmation key entered does not match the one associated with this e-mail address. Please try again.'])
			raise forms.ValidationError('confkey')
		return self.cleaned_data


def confirm(request):
	"""
	Method to verify confirmation keys and activate user accounts.
	"""
	username = request.REQUEST.get('username')
	if username:
		form = ConfirmationForm(request.REQUEST)
		if form.is_valid():
			user = User.objects.get(username=username)
			user.active = True
			user.save()
			request.session.clear()
			return render_to_response('mysmg/confirmed.html', {'form': form}, context_instance=RequestContext(request))
		else:
			return render_to_response('mysmg/confirm.html', {'form': form}, context_instance=RequestContext(request))			
	else:
		form = ConfirmationForm()
		return render_to_response('mysmg/confirm.html', {'form': form}, context_instance=RequestContext(request))

"""
User Authentication Classes and Methods
"""

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	def clean_username(self):
		username = self.cleaned_data['username']
		if not User.objects.filter(username=username):
			raise forms.ValidationError('nouser')
		return username
	def clean_password(self):
		username = self.data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username, password=md5.new(password).hexdigest()):
			raise forms.ValidationError('badpassword')
		return password

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.get(username=data['username'], password=md5.new(data['password']).hexdigest())
				if user.active:
					request.session.clear()
					request.session['authenticated'] = True
					request.session['username'] = data['username']
					return HttpResponseRedirect('/mysummitmedicalgroup/')
				else:
					return render_to_response('mysmg/login.html', {'form': form, 'error': 'inactive'}, context_instance=RequestContext(request))
			except User.DoesNotExist:
				return render_to_response('mysmg/login.html', {'form': form, 'error': 'nouser'}, context_instance=RequestContext(request))
		else:
			return render_to_response('mysmg/login.html', {'form': form}, context_instance=RequestContext(request))
	else:
		if request.session.get('authenticated'):
			user = User.objects.get(username=request.session['username'])
			return render_to_response('mysmg/login_already.html', {'user': user}, context_instance=RequestContext(request))
		else:
			form = LoginForm()
			return render_to_response('mysmg/login.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
	"""
	AJAX return method for handling MySMG logouts.
	"""
	
	request.session['username'] = None
	request.session['authenticated'] = False
	if request.GET.get('redirect'):
		return HttpResponseRedirect(request.GET['redirect'])
	return HttpResponseRedirect('/')


"""
Forgot Password Classes and Methods
"""


class ForgotForm(forms.Form):
	"""
	Class for generating the user password reset form
	"""
	username = forms.CharField(max_length=50)
	def clean(self):
		try:
			username = self.cleaned_data['username']
		except KeyError:
			self._errors['username'] = ErrorList(['The e-mail address field is required.'])
			raise forms.ValidationError('username')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			self._errors['username'] = ErrorList(['Your e-mail address does not match any profiles in our system. Please try again.'])
			raise forms.ValidationError('username')
		if not user.active:
			self._errors['username'] = ErrorList(['The account for the e-mail address you have entered is not active. The most likely reason is that the account has not been confirmed. Please check your e-mail inbox for a confirmation message that has instructions for activating this account. Note: If you have not received this mail, be sure to check your spam folders and confirm that you can recieve e-mails from register@summitmedicalgroup.com.'])
			raise forms.ValidationError('username')			
		return self.cleaned_data


def forgot(request):
	import random
	from django.core.mail import EmailMessage
	from urllib import quote, unquote
	"""
	Method to verify confirmation keys and activate user accounts.
	"""
	username = request.REQUEST.get('username')
	if username:
		form = ForgotForm(request.REQUEST)
		if form.is_valid():
			user = User.objects.get(username=username)
			new_password = '%c%c-%d%d%d-%c%c' % (chr(random.randrange(65, 91)), chr(random.randrange(65, 91)), random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), chr(random.randrange(65, 91)), chr(random.randrange(65, 91)))
			user.new_password = md5.new(new_password).hexdigest()
			confkey = '%d%d%d-%c%c' % (random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), chr(random.randrange(65, 91)), chr(random.randrange(65, 91)))
			user.confkey = confkey
			user.save()	
			if user.first_name:
				salutation = user.first_name
			else:
				salutation = user.username
			subject = 'Summit Medical Group Account Confirmation'
			message = "Dear %s,\n\nWe received a request to reset the password for your My Summit Medical Group account. Your new password is: %s.\n\nTo activate the new password, please click the link below to confirm. If the link does not work, please cut and paste the following URL into your browser's location:\n\nhttp://%s/mysummitmedicalgroup/password-reset/?username=%s&confkey=%s\n\nYou must confirm this password request to use the new password. If you did not request a new password, you can continue to use your previous password.\n\nPlease consult the Help page on the site if you have additional questions.\n\nSincerely,\n\nSummit Medical Group" % (salutation, new_password, request.META['HTTP_HOST'], user.username, confkey)
			msg = EmailMessage(subject, message, 'register@summitmedicalgroup.com', [user.username])
			msg.fail_silently = True
			msg.send()
			return render_to_response('mysmg/edit_reset_confirm.html', {'user': user}, context_instance=RequestContext(request))
		else:
			return render_to_response('mysmg/forgot_password.html', {'form': form}, context_instance=RequestContext(request))			
	else:
		form = ForgotForm()
		return render_to_response('mysmg/forgot_password.html', {'form': form}, context_instance=RequestContext(request))


"""
Edit Profile Classes and Methods
"""

class EditForm(forms.Form):
	import re
	zip_re = re.compile(r'\d\d\d\d\d(-\d\d\d\d){0,1}')
	
	current_username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'inp'}))
	current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inp'}))
	
	password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'inp'}))
	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'inp'}))
	
	first_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	middle_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	last_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={'class':'inp'}))
	zipcode = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class':'inp inp_short'}))
	
	security_question = forms.ChoiceField(required=False, choices=(("", "Select one"), ("What is your mother's maiden name?", "Mother's Maiden Name"), ("What is your favorite pet's name?", "Favorite Pet's Name"), ("What is your town/city of birth?", "Birthplace (City/Town)")))
	security_answer = forms.CharField(max_length=50, required=False)
	
	contact = forms.ChoiceField(choices=((1, "Yes, I'd like to subscribe."), (0, "No, thank you.")), widget=forms.RadioSelect(attrs={'class':'radio_buttons'}))
	def clean_current_username(self):
		try:
			user = User.objects.get(username=self.cleaned_data['current_username'])
			return self.cleaned_data['current_username']
		except User.DoesNotExist:
			raise forms.ValidationError('current_username')
	def clean_phone(self):
		phonestr = '(%s)-%s-%s' % (self.cleaned_data.get('phone_area'), self.cleaned_data.get('phone_exchange'), self.cleaned_data.get('phone_number'))
		return phonestr
	def clean_zipcode(self):
		zipcode = self.cleaned_data.get('zipcode')
		if zipcode:
			match = self.zip_re.match(zipcode)
			if not match:
				raise forms.ValidationError('zipcode')
		return zipcode
	def clean(self):
		if self.cleaned_data.get('password') and self.cleaned_data.get('password2'):
			p1 = self.cleaned_data['password']
			p2 = self.cleaned_data['password2']
			if len(p1) < 6 or len(p1) > 20:
				self._errors["password2"] = ErrorList(['password2'])
				raise forms.ValidationError('password2')
			if p1 != p2:
				self._errors["password2"] = ErrorList(['password2'])
				raise forms.ValidationError('password2')
		return self.cleaned_data

def edit(request):
	import random
	from django.core.mail import EmailMessage
	from urllib import quote, unquote
	authenticated = request.session.get('authenticated')					
	if authenticated:
		user = User.objects.get(username=request.session['username'])
		if request.method == 'POST':
			form = EditForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				user.first_name = data['first_name']
				user.middle_name = data['middle_name']
				user.last_name = data['last_name']
				user.zipcode = data['zipcode']
				user.security_question = data['security_question']
				user.security_answer = data['security_answer']
				user.contact = data['contact']
				if data['password']:
					user.new_password = md5.new(data['password']).hexdigest()
					confkey = '%d%d%d-%c%c' % (random.randrange(0,10), random.randrange(0,10), random.randrange(0,10), chr(random.randrange(65, 91)), chr(random.randrange(65, 91)))
					user.confkey = confkey
					user.save()	
					if user.first_name:
						salutation = user.first_name
					else:
						salutation = user.username
					subject = 'Summit Medical Group Account Confirmation'
					message = "Dear %s,\n\nWe received a request to reset the password for your My Summit Medical Group account. To activate the new password, please click the link below to confirm. If the link does not work, please cut and paste the following URL into your browser's location:\n\nhttp://%s/mysummitmedicalgroup/password-reset/?username=%s&confkey=%s\n\nYou must confirm this password request to use the new password. If you did not request a new password, you can continue to use your previous password.\n\nPlease consult the Help page on the site if you have additional questions.\n\nSincerely,\n\nSummit Medical Group" % (salutation, request.META['HTTP_HOST'], user.username, confkey)
					msg = EmailMessage(subject, message, 'register@summitmedicalgroup.com', [user.username])
					msg.fail_silently = True
					msg.send()
					return render_to_response('mysmg/edit_reset_confirm.html', {'user': user}, context_instance=RequestContext(request))
				else:
					user.new_password = ''
					user.save()
					return render_to_response('mysmg/edit_confirm.html', {'user': user}, context_instance=RequestContext(request))
			else:
				return render_to_response('mysmg/edit.html', {'form': form}, context_instance=RequestContext(request))
		else:
			form = EditForm(initial={'first_name': user.first_name, 'middle_name': user.middle_name, 'last_name': user.last_name, 'zipcode': user.zipcode, 'security_question': user.security_question, 'security_answer': user.security_answer, 'contact': user.contact})
			return render_to_response('mysmg/edit.html', {'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/mysummitmedicalgroup/login/')


class ResetForm(forms.Form):
	"""
	Class for generating the user password reset form
	"""
	username = forms.CharField(max_length=50)
	confkey = forms.CharField(max_length=6)
	def clean(self):
		try:
			username = self.cleaned_data['username']
		except KeyError:
			self._errors['username'] = ErrorList(['The e-mail address field is required.'])
			raise forms.ValidationError('username')
		try:
			confkey = self.cleaned_data['confkey']
		except KeyError:
			self._errors['confkey'] = ErrorList(['The confirmation key field is required.'])
			raise forms.ValidationError('confkey')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			self._errors['username'] = ErrorList(['Your e-mail address does not match any profiles in our system. Please verify that you have typed it correctly.'])
			raise forms.ValidationError('username')
		if confkey != user.confkey:
			self._errors['confkey'] = ErrorList(['The confirmation key entered does not match the one associated with this e-mail address. Please try again.'])
			raise forms.ValidationError('confkey')
		return self.cleaned_data


def reset(request):
	"""
	Method to verify confirmation keys and activate user accounts.
	"""
	username = request.REQUEST.get('username')
	if username:
		form = ResetForm(request.REQUEST)
		if form.is_valid():
			user = User.objects.get(username=username)
			user.password = user.new_password
			user.new_password = ''
			user.save(newpass=True)
			request.session.clear()
			return render_to_response('mysmg/reset_confirmed.html', {'form': form}, context_instance=RequestContext(request))
		else:
			return render_to_response('mysmg/reset_confirm.html', {'form': form}, context_instance=RequestContext(request))			
	else:
		form = ResetForm()
		return render_to_response('mysmg/reset_confirm.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def export(request):
	users = User.objects.all()
	return render_to_response('admin/mysmg/user/export_users.html', {'users': users}, context_instance=RequestContext(request), mimetype='application/ms-excel')
