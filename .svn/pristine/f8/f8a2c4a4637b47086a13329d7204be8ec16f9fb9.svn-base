from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings

from smgsite.pages.models import Template, Directory, Page

DEFAULT_TEMPLATE = 'pages/default.html'

def dispatch(request):
	"""
	This method catches 404 errors and looks to see if there is a Page object
	to be served for the request.
	
	This technique was dropped from phase ii .. this method was never finished.
	"""
	print "Found dispatch service!"
	template = "services/" + service + "/" + subservice + ".html"
	if request.user.is_authenticated():
		service = Service.qa_objects.get(urlname=service)
		service.qa = True
	else:
		service = Service.objects.get(urlname=service)
		service.qa = False
	try:
		f = open(TEMPLATE_ROOT + '/' + template, 'r')
		ttext = ''.join(f.readlines())
		f.close()
	except IOError:
		raise Http404
	title = 'Service Content'
	m = title_re.match(ttext)
	if m:
		title = m.group(2)
	pages = ['services/%s/subservice.html' % service.urlname, 'services/subservice.html']
	return render_to_response(pages, {'template': template, 'title': title, 'service': service, 'subservice': subservice}, context_instance=RequestContext(request))



def get_page(request, url):

    """
		- Detect 404 in middleware.
		- Try to get page by urlname.
		- Render page with template.
    """

    if not url.startswith('/'):
        url = '/' + url
    try:
        page = get_object_or_404(Page, url=url, active='1')
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            page = get_object_or_404(Page, url=url, active='1')
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise

    if page.template_name:
        template = loader.select_template((page.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)


    ctx = RequestContext(request, {
        'page': page,
        'content': page.content,
    })

    return HttpResponse(template.render(ctx))
