from django import forms
from django.utils.encoding import smart_text

from smgsite.doctors.models import Doctor, Specialty, Language, Hospital
from smgsite.services.models import Service
from smgsite.site.models import Location

SELECT_LABEL = "Select From List"

INPUT_CLASS = {'class':'form-control'}



def get_facet_choices(queryset, value_name, name, operator="exact"):
    res = [('',SELECT_LABEL)]
    #model_name = queryset.model.__name__.lower()
    for obj in queryset:
        facet = "%s_%s:%s" % (name, operator, getattr(obj, value_name))
        res.append((facet, smart_text(obj)))
    return res

def get_city_choices():
    res = [('',SELECT_LABEL)]
    city_list = Location.objects.filter(display=1).order_by('city').values_list('city', flat=True).distinct()
    for city in city_list:
        facet = "%s_%s:%s" % ("locations", "exact", city)
        res.append((facet, smart_text(city)))
    return res

class DoctorFinderForm(forms.Form):
    location = forms.ChoiceField(
        choices=get_city_choices(), 
        widget=forms.Select(attrs=INPUT_CLASS))
    
    specialties = forms.ChoiceField(
        choices=get_facet_choices(Service.objects.all(), 'name', 'services'), 
        widget=forms.Select(attrs=INPUT_CLASS))

    languages = forms.ChoiceField(
        choices=get_facet_choices(Language.objects.all(), 'language', 'languages'),
        widget=forms.Select(attrs=INPUT_CLASS))

    hospitals = forms.ChoiceField(
        choices=get_facet_choices(Hospital.objects.all(), 'hospital', 'hospitals'), 
        widget=forms.Select(attrs=INPUT_CLASS))
    
    gender = forms.ChoiceField(
        widget=forms.RadioSelect(attrs=INPUT_CLASS),
        choices=Doctor.GENDER)

    def __init__(self, *args, **kwargs):
        super(DoctorFinderForm, self).__init__(*args, **kwargs)

    #def add_prefix(self, field_name):
        #return super(DoctorFinderForm, self).add_prefix('selected_facets')


class ConditionFinderForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs=INPUT_CLASS))


class DoctorAdminForm(forms.ModelForm):
    
    class Meta:
        model = Doctor
        widgets = {
            'languages': forms.SelectMultiple(attrs={'class': 'select2-lang', 'style': 'width:220px'}),
        }
        



