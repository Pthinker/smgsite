from django.template import RequestContext
from django.shortcuts import render_to_response
from smgsite.doctors.models import Doctor

def test(request):
        doctors = Doctor.qa_objects.order_by('?')[:10]
        return render_to_response('minisite/test.html', {'doctors': doctors}, context_instance=RequestContext(request))

