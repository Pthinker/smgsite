from django import forms


from smgsite.services.models import Service, ServiceGroup

INPUT_CLASS = {'class':'form-control service_list_select'}
SELECT_LABEL = "Select a Service"

def get_grouped_services():
    res = [('',SELECT_LABEL)]
    for group in ServiceGroup.objects.all():
        res.append((group.name, [(service.urlname, service.name) for service in group.services.all()]))
    return res

def get_service_list():
    res = [('',SELECT_LABEL)]
    for service in Service.objects.all():
        res.append((service.urlname, service.name))

    return res

class ServiceForm(forms.Form):
    service_list = forms.CharField(
        widget=forms.Select(choices=get_service_list(), attrs=INPUT_CLASS)
        )
