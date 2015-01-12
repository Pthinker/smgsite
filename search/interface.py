import sys
import os
import stat
import re
import codecs
from socket import *
from django.db import models
from django.core.paginator import Paginator
from smgsite.settings import TEMPLATE_ROOT, SEARCH_HOST, SEARCH_PORT
from smgsite.search.containers import *

OPTIMIZE_ON_POST = True

title_re = re.compile(r'^(.*){# TITLE: (.*?) #}(.*)$', re.S)
keywords_re = re.compile(r'^(.*){# KEYWORDS: (.*?) #}(.*)$', re.S)


def recv_basic(the_socket):
	total_data=[]
	while True:
		data = the_socket.recv(4096)
		if not data: break
		total_data.append(data)
	return ''.join(total_data)


def search(count, kind, model, order, name, body):
	"""
	Method to search the lucene search index.		
	"""
	# Ensure no newlines in the body
	body = body.replace('\n', ' ')
	message = "SEARCH\n%s\n%s\n%s\n%s\n%s\n%s\n" % (count, kind, model, order, name, body)
	message = message.encode('ascii', 'ignore')
	
	serverHost = SEARCH_HOST
	serverPort = SEARCH_PORT
	
	s = socket(AF_INET, SOCK_STREAM)

	s.connect((serverHost, serverPort))
	s.send(message)
	data = recv_basic(s).decode('utf-8')
	lines = data.strip().split('\n')
	return (lines[0], [Result(line.split(':', 3)) for line in lines[1:]])							


def reindex():
	"""
	Method to reindex all search content:
	
	Iterates through all searchable posting text to the search engine.	
	"""
	OPTIMIZE_ON_POST = False
	# Iterate through all applications and all models
	for app in models.get_apps():
		model_list = models.get_models(app)
		if not model_list:
			continue
		for model in model_list:
			print "Trying model %s" % model
			try:
				# Test if the model is a placeholder for search
				model.search_placeholder
			except AttributeError:
				try:
					# Test if the model supports the search_index method
					model.search_index
				except AttributeError:
					continue
				# Iterate through all instances of the model and construct the search fields
				p = Paginator(model.objects.all(), 10000)
				for i in p.page_range:
					page = p.page(i)
					for value in page.object_list:
						value.index()
			"""
			Subpages are now all handled through the Page model, not the filesystem.
			try:
				# Test if the model allows indexes subpages
				if model.has_subpages:
					index_subpages(model)
			except AttributeError:
				continue"""
	optimize()
	OPTIMIZE_ON_POST = True


def find_keywords():
	"""
	Method to find a list of all keywords for all searchable objects.
	"""
	
	klist = []
	# Iterate through all applications and all models
	for app in models.get_apps():
		model_list = models.get_models(app)
		if not model_list:
			continue
		for model in model_list:
			try:
				# Test if the model has keywords
				model.keyword_index
			except AttributeError:
				continue
			# Iterate through all instances of the model and fetch the keywords
			for value in model.objects.all():
				searchkey = value.keyword_index()
				if searchkey.name:
					klist.append(Keyword(model.__name__, searchkey))
	return klist


def post(model, searchkey):
	"""
	Method to post a new searchable item to the lucene search index.		
	"""
	searchkey.body = searchkey.body.replace('\n', ' ')
	message = u"POST\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (model, searchkey.key, searchkey.url, searchkey.order, searchkey.display, searchkey.name, searchkey.body)
	message = message.encode('utf-8', 'ignore')
	serverHost = SEARCH_HOST
	serverPort = SEARCH_PORT
	
	try:
		s = socket(AF_INET, SOCK_STREAM)
		
		s.connect((serverHost, serverPort))
		s.send(message)
		data = s.recv(4096)
		data = data.decode('utf-8', 'ignore')
		s.close()
		if OPTIMIZE_ON_POST:
			optimize()
	except error, e:
		print "ERROR: Socket error commuicating with search engine in post; error %s" % e


def delete(model, key):
	"""
	Method to remove a searchable item from the lucene search index.		
	"""
	
	message = u"DELETE\n%s\n%s\n" % (model, key)
	message = message.encode('ascii', 'ignore')
	
	serverHost = SEARCH_HOST
	serverPort = SEARCH_PORT
	
	s = socket(AF_INET, SOCK_STREAM)

	s.connect((serverHost, serverPort))
	s.send(message)
	data = s.recv(4096)
	s.close()


def optimize():
	"""
	Method to send an optimize request to the server.		
	"""
	
	message = "OPTIMIZE\n"
	
	serverHost = SEARCH_HOST
	serverPort = SEARCH_PORT
	
	s = socket(AF_INET, SOCK_STREAM)

	s.connect((serverHost, serverPort))
	s.send(message)
	data = s.recv(4096)
	s.close()

"""
def index_subpage(filepath, template_path, item_url):
	print "File is %s" % filepath
	f = codecs.open(filepath, 'r', 'utf-8')
	body = u''.join(f.readlines())
	f.close()
	m = title_re.match(body)
	if m:
		title = m.group(2)
		postbody = u"%s%s" % (m.group(1), m.group(3))
		# Create a (key, url, order, display, name, body) tuple with text for indexing
		urlfile = filepath[len(TEMPLATE_ROOT)+len(template_path)+2:filepath.rindex('.')]
		url = '/%s/%s/' % (item_url, urlfile)
		print "URL is %s" % url
		refname = 'Editor.%s' % item_url
		#print "Posting %s %s %s %s %s %s %s" % (refname, '%s-%s' % (refname, filepath), url, title, title, title, postbody)
		searchkey = SearchKey('%s-%s' % (refname, filepath), url, title, title, title, postbody)
		post(refname, searchkey)
		m = keywords_re.match(body)
		if m:
			keywords = m.group(2)
			#print "Posting %s %s %s %s %s %s %s" % ('Keyword', 'Keyword-%s' % (filepath), url, title, title, keywords, keywords)
			searchkey = SearchKey('Keyword-%s' % (filepath), url, title, title, keywords, keywords)
			post('Keyword', searchkey)


def index_subpages(model):
	path = '%s/%s' % (TEMPLATE_ROOT, model.template_path)
	files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		if dirpath.find('.svn') >= 0:
			continue
		for name in filenames:
			filepath = '%s/%s' % (dirpath, name)
			if stat.S_ISREG(os.stat(filepath).st_mode):
				index_subpage(filepath, model.template_path, model.item_url)

"""
