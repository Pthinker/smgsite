import re

from django import forms

from smgsite.events.models import Event, Eventtime, Registration, Referrer, Class

phone_re = re.compile(r'\({0,1}(\d\d\d)\){0,1}[ -]{0,1}(\d\d\d)[ -]{0,1}(\d\d\d\d)')
zip_re = re.compile(r'\d\d\d\d\d(-\d\d\d\d){0,1}')

class EventForm(forms.Form):
    eventdates = forms.MultipleChoiceField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.CharField(max_length=3, required=False)
    city = forms.CharField(max_length=50)
    state = forms.ChoiceField(choices=Registration.STATES, initial='NJ')
    zipcode = forms.CharField(max_length=10)
    #guests = forms.IntegerField(min_value=0, max_value=99)
    email = forms.EmailField()
    main_phone_area = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_main_phone_exchange"));'}))
    main_phone_exchange = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_main_phone_number"));'}))
    main_phone_number = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'size':'4', 'onkeyup':'moveto(this, 4, document.getElementById("id_main_phone_extn"));'}))
    main_phone_extn = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={'size':'4'}))
    alt_phone_area = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_alt_phone_exchange"));'}))
    alt_phone_exchange = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'size':'3', 'onkeyup':'moveto(this, 3, document.getElementById("id_alt_phone_number"));'}))
    alt_phone_number = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={'size':'4', 'onkeyup':'moveto(this, 4, document.getElementById("id_alt_phone_extn"));'}))
    alt_phone_extn = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={'size':'4'}))
    main_phone = forms.CharField(required=False, widget=forms.HiddenInput())
    alt_phone = forms.CharField(required=False, widget=forms.HiddenInput())
    sendmail = forms.BooleanField(required=False)
    referrer = forms.ChoiceField(choices=[('', 'Choose one')] + [(a.values()[0], a.values()[0]) for a in Referrer.objects.values('name').order_by('order')])
    def clean_eventdates(self):
        if not self.cleaned_data['eventdates']:
            raise forms.ValidationError('No event was selected.')
        return self.cleaned_data['eventdates']
    def clean_age(self):
        if self.cleaned_data['age']:
            try:
                age = int(self.cleaned_data['age'])
            except ValueError:
                raise forms.ValidationError('Age must be numeric')
            return age
        return None
    def clean_main_phone(self):
        phonestr = '(%s)-%s-%s' % (self.cleaned_data.get('main_phone_area'), self.cleaned_data.get('main_phone_exchange'), self.cleaned_data.get('main_phone_number'))
        match = phone_re.match(phonestr)
        if not match:
            raise forms.ValidationError('Daytime phone number is not in the required format.')
        extn = ''
        if self.cleaned_data.has_key('main_phone_extn') and self.cleaned_data['main_phone_extn']:
            extn = 'x%s' % self.cleaned_data.get('main_phone_extn')
        return '%s-%s-%s %s' % (match.group(1), match.group(2), match.group(3), extn)
    def clean_alt_phone(self):
        if not self.cleaned_data.has_key('alt_phone_area') or not self.cleaned_data['alt_phone_area']:
            return ''
        phonestr = '(%s)-%s-%s' % (self.cleaned_data.get('alt_phone_area'), self.cleaned_data.get('alt_phone_exchange'), self.cleaned_data.get('alt_phone_number'))
        match = phone_re.match(phonestr)
        if not match:
            raise forms.ValidationError('Alternate phone number is not in the required format.')
        extn = ''
        if self.cleaned_data.has_key('alt_phone_extn') and self.cleaned_data['alt_phone_extn']:
            extn = 'x%s' % self.cleaned_data.get('alt_phone_extn')
        return '%s-%s-%s %s' % (match.group(1), match.group(2), match.group(3), extn)
    def clean_zipcode(self):
        match = zip_re.match(self.cleaned_data['zipcode'])
        if not match:
            raise forms.ValidationError('Zip code is not in 5 digit or 5-4 digit format.')
        return self.cleaned_data['zipcode']
    #def clean_guests(self):
    #   number = self.cleaned_data['guests']
    #   if number < 0 or number > 99:
    #       raise forms.ValidationError('Number of guests is out of range.')
    #   return number
    def clean_sendmail(self):
        if self.cleaned_data['sendmail'] == 1:
            return 'T'
        return 'F'