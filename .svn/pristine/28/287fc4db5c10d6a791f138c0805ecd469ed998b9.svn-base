
from django.shortcuts import render_to_response
from django.template import RequestContext

def redirect(request, path):
        if path == 'extensivist':
                return render_to_response('site/redirect.html', {'path': '/service/Extensivist-Medicine/'}, context_instance=RequestContext(request))
        elif path == 'bp':
                return render_to_response('site/redirect.html', {'path': '/feature/Nutrition/Eating-for-Healthy-Blood-Pressure/'}, context_instance=RequestContext(request))


