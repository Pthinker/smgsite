from django.db.models import Q
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from smgsite.careers.models import Career

class CareersForm(forms.Form):
	job_title = forms.ChoiceField(required=False, widget=forms.Select(attrs={'style':'width: 175px;','onfocus':'window.dropdown_menu_hack(this);'}), choices=[('', 'All available jobs')] + [(a.values()[0], a.values()[0]) for a in Career.objects.values('job_title').distinct().order_by('job_title')])
	department = forms.ChoiceField(required=False, widget=forms.Select(attrs={'style':'width: 175px;','onfocus':'window.dropdown_menu_hack(this);'}), choices=[('', 'All departments')] + [(a.values()[0], a.values()[0]) for a in Career.objects.values('department').distinct().order_by('department')])
 	shift_type = forms.ChoiceField(required=False, widget=forms.Select(attrs={'style':'width: 175px;','onfocus':'window.dropdown_menu_hack(this);'}), choices=[('', 'All shift types')] + [(a[0], a[1]) for a in Career.SHIFT_TYPE])

def careers_search(request):
	if request.GET.get('search'):
		form = CareersForm(request.GET)
		results = None
		if form.is_valid():
			data = form.cleaned_data
			job_title = data['job_title']
			department = data['department']
			shift_type = data['shift_type']
			qset = Q()
			if job_title:
				qset = qset & Q(job_title=job_title)
			if department:
				qset = qset & Q(department=department)
			if shift_type:
				qset = qset & Q(shift_type=shift_type)
			results = Career.objects.filter(qset).order_by('job_title')
		return render_to_response('careers/careers_search.html', {'results': results, 'form': form, 'searched': True}, context_instance=RequestContext(request))
	else:
		form = CareersForm()
		return render_to_response('careers/careers_search.html', {'form': form, 'searched': False}, context_instance=RequestContext(request))
