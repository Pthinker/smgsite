
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from smgsite.services.models import Service, ServiceGroup, ServiceGroupDetail
from smgsite.services.forms import ServiceForm
from smgsite.doctors.models import Doctor

def service_groups_view(request):
    """
    Show service groups.
    """
    service_groups = ServiceGroup.objects.all().order_by('order')
    ctx = {
        'groups': service_groups,
        'service_form': ServiceForm(),
        }
    return render(request, 'services/service_groups.html', ctx)


def service_group_view(request, urlname):
    """
    Services within selected group.
    """
    service_group = get_object_or_404(ServiceGroup, urlname=urlname)
    services = ServiceGroupDetail.objects.filter(servicegroup=service_group)
    return render(request, 'services/service_group.html', {'group': service_group, 'services': services})

def services_view(request):
    """
    List of all Services.
    """
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})

def service_detail_view(request, urlname):
    service_qs = Service.objects.filter(active='1')
    service = get_object_or_404(service_qs, urlname=urlname)

    service_group_details = ServiceGroupDetail.objects.all()
    service_groups = ServiceGroup.objects.all()
    template_name = 'services/%s' % service.template.name
    service_doctors = Doctor.objects.order_by('last_name').filter(status='D').filter(Q(title_service=service) | Q(services=service)).distinct()
    ctx = {
        'service': service, 
        'doctors': service_doctors,
        'service_group_details': service_group_details,
        'quicklook_form': ServiceForm(),
        'quicklook_form2': ServiceForm(prefix="2"),
        'service_groups': service_groups,
    }
    return render(request, template_name, ctx)