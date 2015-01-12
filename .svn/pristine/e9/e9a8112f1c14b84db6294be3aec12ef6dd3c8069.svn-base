from django.http import Http404, HttpResponse
from django.conf import settings
from django.template import loader, TemplateDoesNotExist, RequestContext

class Custom404Middleware(object):
    def process_response(self, request, response):
        if response.status_code != 404 or request.path =='/':
            return response
        try:
            template_name = '%s_404.html' % request.path.split('/')[1]
            t = loader.get_template(template_name) 
            return HttpResponse(
                content=t.render(RequestContext(request)), 
                content_type='text/html; charset=utf-8', 
                status=404)
           
        except TemplateDoesNotExist:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response