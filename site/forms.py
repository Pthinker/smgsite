from django import forms

from smgsite.site.models import Location


INPUT_CLASS = {'class':'form-control'}
SELECT_LABEL = "Select From List"

def get_city_choices():
    # using mysql so proper distinct on does not work
    cities = Location.objects.filter(display=Location.SHOW).order_by('city').values_list('city', flat=True).distinct()
    res = [('',SELECT_LABEL)]
    for city in cities:
        res.append((city, city))
    return res

class CitySelectForm(forms.Form):
    city = forms.ChoiceField(
        choices=get_city_choices(),
        widget=forms.Select(attrs=INPUT_CLASS))