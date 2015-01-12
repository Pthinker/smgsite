from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from smgsite.cms import models as cms
from smgsite.search.interface import find_keywords

@login_required
def index(request):
	(additions, deletions, changes) = cms.find_objects()
	return render_to_response('cms/index.html', {'additions': additions, 'deletions': deletions, 'changes': changes, 'root_path': '/admin/'}, context_instance=RequestContext(request))


@login_required
def change(request, pk):
	cms.change(pk)
	return HttpResponseRedirect(reverse('smgsite.cms.views.index'))


@login_required
def unchange(request, pk):
	cms.unchange(pk)
	return HttpResponseRedirect(reverse('smgsite.cms.views.index'))


@login_required
def add(request, app, model, pk):
	cms.add(app, model, pk)
	return HttpResponseRedirect(reverse('smgsite.cms.views.index'))


@login_required
def delete(request, app, model, pk):
	cms.delete(app, model, pk)
	return HttpResponseRedirect(reverse('smgsite.cms.views.index'))


@login_required
def keywords(request):
	""" Generate a report of all keywords in the system """
	keywords = find_keywords()
	#(keywords, model.__name__, display, url))
	return render_to_response('cms/keywords.html', {'keywords': keywords}, context_instance=RequestContext(request))

