import os
import stat
import re
import codecs
from HTMLParser import HTMLParser
from urllib import urlopen
from django.template import RequestContext, Context, Template, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from smgsite.settings import TEMPLATE_ROOT, MEDIA_ROOT, MEDIA_URL
from smgsite.cms import models as cms
from smgsite.search.interface import title_re, keywords_re
from smgsite.site.models import MediaCategory, Image, MediaFile
from smgsite.urls import urlpatterns


dirname_re = re.compile(r'^[-\w]+$')
filename_re = re.compile(r'^[-\w]+\.html$')
url_re = re.compile(r'^\^([^\$\(]*).*')

models = {'services': 'service'}

class File(object):
	def __init__(self, isdir, path, name, size=0):
		self.__dict__.update(locals())
		del self.self


class SiteParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			a = dict(attrs)
			if a.has_key('href'):
				link = a['href']
				if link and not link.startswith('#') and not link.startswith('http'):
					try:
						self.links[link] = True
					except AttributeError:
						self.links = dict()
						self.links[link] = True


@login_required
def view(request, path):
	f = file(path)
	l = ''.join(f.readlines())
	t = Template(l)
	c = Context()
	return HttpResponse(t.render(c))

@login_required
def source(request, path):
	f = file(path)
	l = ''.join(f.readlines())
	return HttpResponse(l, mimetype='text/plain')

@login_required
def edit(request, path):
	if request.method == 'POST':
		t = request.POST['title']
		l = ''
		if t:
			# This file will be indexed for search
			l = '{# TITLE: %s #}' % t
			k = request.POST['keywords']
			if k:
				l += '{# KEYWORDS: %s #}' % k
		l += request.POST['content']
		f = codecs.open(path, 'w', 'utf-8')
		f.write(l)
		f.close()
		basepath = path[len(TEMPLATE_ROOT)+1:]
		basepath = basepath[0:basepath.find('/')]
		print path, basepath
		if models.has_key(basepath):
			modelpath = models[basepath]
		else:
			modelpath = basepath
		#index_subpage(path, basepath, modelpath)
		path = path[0:path.rfind('/')]
		return HttpResponseRedirect(reverse('smgsite.editor.views.path_index', args=(path, '')))
	else:
		f = codecs.open(path, 'r', 'utf-8')
		l = ''.join(f.readlines())
		f.close()
		m = title_re.match(l)
		title = ''
		keywords = ''
		if m:
			title = m.group(2)
			l = "%s%s" % (m.group(1), m.group(3))
			m = keywords_re.match(l)
			if m:
				keywords = m.group(2)
				l = "%s%s" % (m.group(1), m.group(3))
		return render_to_response('editor/edit.html', {'new': False, 'title': title, 'keywords': keywords, 'content': l}, context_instance=RequestContext(request))

@login_required
def newdir(request):
	path = request.GET['path']
	filename = request.GET['filename']
	if not dirname_re.match(filename):
		message = urlquote('A directory name may contain only letters, numbers, underscores or dashes.')
		return HttpResponseRedirect(reverse('smgsite.editor.views.path_index', args=(path, message)))
	filename = path + "/" + filename
	os.mkdir(filename)
	return HttpResponseRedirect(reverse('smgsite.editor.views.path_index', args=(path, '')))

@login_required
def new(request):
	if request.method == 'POST':
		path = request.GET['path']
		filename = path + "/" + request.GET['filename']
		t = request.POST['title']
		l = ''
		if t:
			# This file will be indexed for search
			l = '{# TITLE: %s #}' % t
			k = request.POST['keywords']
			if k:
				l += '{# KEYWORDS: %s #}' % k
		l += request.POST['content']
		f = codecs.open(filename, 'w', 'utf-8')
		f.write(l)
		f.close()
		return HttpResponseRedirect(reverse('smgsite.editor.views.path_index', args=(path, '')))
	else:
		path = request.GET['path']
		filename = request.GET['filename']
		if not filename_re.match(filename):
			message = urlquote('A filename may contain only letters, numbers, underscores or dashes, and must end with .html.')
			return HttpResponseRedirect(reverse('smgsite.editor.views.path_index', args=(path, message)))
		filename = path + "/" + filename
		l = ''
		return render_to_response('editor/edit.html', {'new': True, 'filename': filename, 'content': l}, context_instance=RequestContext(request))

@login_required
def path_index(request, message, path):
	up = True
	if path == TEMPLATE_ROOT:
		up = False
	files = []
	for name in os.listdir(path):
		if not name[0] == '.':
			files.append(File(stat.S_ISDIR(os.stat(path + '/' + name).st_mode), path, name))
	files.sort(cmp=lambda x,y: cmp(x.name,y.name))
	updir = path[0:path.rfind('/')]
	return render_to_response('editor/dir.html', {'up': up, 'files': files, 'curpath': path, 'updir': updir, 'message': message}, context_instance=RequestContext(request))


@login_required
def index(request):
	return path_index(request, '', TEMPLATE_ROOT + '/services')


@login_required
def fckbrowser(request):
	command = request.GET['Command']
	ctype = request.GET['Type']
	path = request.GET['CurrentFolder']
	files = []
	folders = []
	if ctype == 'Image':
		if path.startswith('/Images/'):
			if path == '/Images/':
				for category in MediaCategory.objects.all():
					folders.append(File(True, category.category, category.category))
			else:
				path = path[8:-1]
				for image in Image.objects.filter(category__category=path).order_by('name'):
					files.append(File(False, image.image.url, image.name, image.image.size))
		else:
			folders.append(File(True, 'Images', 'Images'))
	elif ctype == 'File':
		if path.startswith('/Other Media/'):
			if path == '/Other Media/':
				for category in MediaCategory.objects.all():
					folders.append(File(True, category.category, category.category))
			else:
				path = path[13:-1]
				for media in MediaFile.objects.filter(category__category=path).order_by('name'):
					files.append(File(True, media.mediafile.url, media.name, media.mediafile.size))
		elif path.startswith('/Website/'):
			while path[-2] == '/':
				path = path[:-1]
			path = path[9:]
			u = urlopen('http://qa:test@qa-smg.syncresis.com/%s' % path)
			p = SiteParser()
			p.feed(u.read())
			links = p.links.keys()
			links.sort()
			folders = [File(True, 'link', '/Website%s' % x) for x in links]
			files = [File(False, x, '/Website%s' % x) for x in links]
		else:
			folders.append(File(True, 'Site Links', 'Website'))
			folders.append(File(True, 'Other Media', 'Other Media'))
	t = loader.get_template('editor/browser.xml')
	c = RequestContext(request, {'folders': folders, 'files': files, 'curpath': path})
	return HttpResponse(t.render(c), mimetype='application/xml')

