from django.db import models
import smgsite.cms.models as cms
from smgsite.search import interface as search
import re

markup_re = re.compile(r'(<[^<]*>|[\W\n])', re.S | re.U)
#keyword_re = re.compile(r'^(\w+\s*)*$', re.U)
#keyword_validator = validators.MatchesRegularExpression(keyword_re)


class Model(object):
	"""
	Superclass for Django Models that are indexed in the search engine.
	
	"""
	def index(self, post=True):
		if self.pk and self.active == u'1' and self.for_update == 0 and post:
			searchkey = self.search_index()
			if searchkey:
				refname = self.__class__.__module__.split('.')[1] + '.' + self.__class__.__name__
				searchkey.name = markup_re.sub(' ', searchkey.name)
				searchkey.body = markup_re.sub(' ', searchkey.body)
				search.post(refname, searchkey)
				try:
					searchkey = self.keyword_index()
					if searchkey and searchkey.name:
						searchkey.name = markup_re.sub(' ', searchkey.name)
						searchkey.body = markup_re.sub(' ', searchkey.body)
						searchkey.key = 'Keyword-%s-%s' % (refname, str(self.pk))
						search.post('Keyword', searchkey)
					else:
						search.delete('Keyword', 'Keyword-%s-%s' % (refname, str(self.pk)))
				except AttributeError:
					pass
		if self.pk and self.for_update == 0 and post and not self.active == u'1':
			refname = self.__class__.__module__.split('.')[1] + '.' + self.__class__.__name__
			search.delete(refname, self.pk)
			search.delete('Keyword', 'Keyword-%s-%s' % (refname, str(self.pk)))
	
	def save(self, preview=True, post=True):
		self.index(post)
		try:
			super(Model, self).save(preview=preview)
		except TypeError:
			super(Model, self).save()
	
	def delete(self):
		refname = self.__class__.__module__.split('.')[1] + '.' + self.__class__.__name__
		search.delete(refname, self.pk)
		search.delete('Keyword', 'Keyword-%s-%s' % (refname, str(self.pk)))
		super(Model, self).delete()


class TestModel(cms.Model, Model, models.Model):
	"""
	This model tests the content management system and the search system together.
	
	>>> from smgsite.search.models import TestModel
	>>> from smgsite.cms.models import Change
	>>> from smgsite.search import interface
	>>> x = TestModel(testa=5, testb='teststring')
	>>> x.save(preview=False)
	>>> (count, results) = interface.search('prefix', 'TestModel', 'alpha', 'tes', '')
	SEARCH
	prefix
	TestModel
	alpha
	tes
    <BLANKLINE>
    <BLANKLINE>
	['0']
	>>> x.for_update = 0
	>>> x.save(preview=False)
	>>> (count, results) = interface.search('prefix', 'TestModel', 'alpha', 'tes', '')
	SEARCH
	prefix
	TestModel
	alpha
	tes
    <BLANKLINE>
    <BLANKLINE>
	['1', 'TestModel:1:none:teststring']
	>>> x.delete(preview=False)
	>>> (count, results) = interface.search('prefix', 'TestModel', 'alpha', 'tes', '')
	SEARCH
	prefix
	TestModel
	alpha
	tes
    <BLANKLINE>
    <BLANKLINE>
	['0']
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.BooleanField(default=True)
	testa = models.IntegerField()
	testb = models.CharField(max_length=25)
	
	def search_index(self):
		# Return a (key, url, order, display, name, body) tuple with text for indexing
		return (self.pk, 'none', self.testb, self.testb, self.testb, self.testb)


