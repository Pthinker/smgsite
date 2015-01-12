import re
import os
import copy
from MySQLdb import IntegrityError
from django import forms
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

"""
The for_update flag has the following values:
0: Normal
1: For delete
2: For addition

Users see all elements with flags 0 and 1. Nothing should disappear from the visible
site until the deletion has been approve.

Administrators see all elements with flags 0 and 2 so they can see how the site will
appear after additions and deletions have been approved.

"""

ACTIVE = u'1'
INACTIVE = u'0'

EXCLUDE = u'1'
INCLUDE = u'0'

class Manager(models.Manager):
	def get_query_set(self):
		return super(Manager, self).get_query_set().filter(active='1', for_update__lte=1)


class QAChanger(object):
	def __init__(self, data):
		self.data = data
	def get(self, *args, **kwargs):
		result = self.data.get(*args, **kwargs)
		result.qa_changes()
		return result
	def complex_filter(self, *args, **kwargs):
		result = self.data.complex_filter(*args, **kwargs)
		if isinstance(result, models.query.QuerySet):
			map(lambda x: x.qa_changes(), result)
		else:
			result.qa_changes()
		return result
	def filter(self, *args, **kwargs):
		result = self.data.filter(*args, **kwargs)
		if isinstance(result, models.query.QuerySet):
			map(lambda x: x.qa_changes(), result)
		else:
			result.qa_changes()
		return result
	def order_by(self, *args, **kwargs):
		result = self.data.order_by(*args, **kwargs)
		if isinstance(result, models.query.QuerySet):
			map(lambda x: x.qa_changes(), result)
		else:
			result.qa_changes()
		return result
	def __getattr__(self, name):
		return getattr(self.data, name)


class QAManager(models.Manager):
	def get_query_set(self):
		data = super(QAManager, self).get_query_set().exclude(for_update=1)
		return QAChanger(data)


def test_change(x, y):
	return ((x != None and x != '') or (y != None and y != '')) and (((not x or not y) and unicode(x) != unicode(y)) or unicode(x) != unicode(y))


class Change(models.Model):
	"""
	Model for database changes.
	
	The CMS holds changes for review before appearing live on the site.
	For new database entries, this is accomplished with the for_update field.
	Changes to existing database entries are stored in the changes table for approval.
	"""
	
	app_name = models.CharField(max_length=25)
	model = models.CharField(max_length=25)
	field = models.CharField(max_length=25)
	key = models.PositiveIntegerField()
	data = models.TextField(null=True)
	date_changed = models.DateField(auto_now_add=True)
	
	class Meta:
		unique_together = (('app_name', 'model', 'field', 'key'),)


class Model(object):
	"""
	Superclass for Django Models that require content management.
	
	This class overrides save and delete to prevent changes from happening
	on the site until they have been approved. It also provides a way to
	give admins a preview of changes before they are approved.
	
	The model cannot be tested directly, but is tested below in the TestModel.
	
	But we can test the crazy CMS logic:
	
	>>> # Do not track empties, or compare them with unicode
	>>> x = None
	>>> y = None
	>>> test_change(x, y)
	False
	>>> x = None
	>>> y = ''
	>>> test_change(x, y)
	False
	>>> x = ''
	>>> y = None
	>>> test_change(x, y)
	False
	>>> x = ''
	>>> y = ''
	>>> test_change(x, y)
	False
	>>> # Track removing a value
	>>> x = u'Hello'
	>>> test_change(x, y)
	True
	>>> y = ''
	>>> test_change(x, y)
	True
	>>> # Track creating a value
	>>> x = None
	>>> y = u'Hello'
	>>> test_change(x, y)
	True
	>>> # Track changing a value
	>>> x = u'Hello'
	>>> y = u'There'
	>>> test_change(x, y)
	True
	>>> # Do not track equivalents
	>>> x = u'Hello'
	>>> y = u'There'
	>>> test_change(x, y)
	True
	>>> x = 'Hello'
	>>> y = 'There'
	>>> test_change(x, y)
	True
	"""
	
	ACTIVE = (
		(ACTIVE, 'Active'),
		(INACTIVE, 'Inactive'),
	)
	
	EXCLUDE = (
		(EXCLUDE, 'Exclude'),
		(INCLUDE, 'Include'),
	)
		
	def qa_changes(self):
		# Apply held changes to a model
		myclass = self.__class__
		app_name = myclass.__module__.split('.')[1]
		for change in Change.objects.filter(app_name=app_name, model=myclass.__name__, key=self.pk):
			setattr(self, change.field, change.data)
	
	def pending(self):
		return self.for_update == 2 or Change.objects.filter(app_name=self.__class__.__module__.split('.')[1], model=self.__class__.__name__, key=self.pk).count() > 0
	
	def changes(self):
		return self.pending()
	changes.short_description = 'Changes Pending Approval'
	changes.boolean = True
	
	def save(self, preview=True, post=True):
		# Save function for holding changes for approval
		if not preview or not self.pk:
			# Changes can be committed immediately
			try:
				super(Model, self).save(post=post)
			except TypeError:
				super(Model, self).save()
		else:
			# The CMS needs to track the change
			myclass = self.__class__
			old = myclass.all_objects.get(pk=self.pk)
			for attr in old.__dict__:
				if attr.endswith('_cache'):
					continue
				app_name = myclass.__module__.split('.')[1]
				#print "Change for %s on app %s" % (attr, app_name)
				#print self
				try:
					c = Change.objects.get(app_name=app_name, model=myclass.__name__, field=attr, key=self.pk)
					x = c.data
				except Change.DoesNotExist:
					c = None
					x = old.__dict__[attr]
				y = self.__dict__[attr]
				if type(y) == bool:
					if y:
						y = 1
					else:
						y = 0
				#print "%s: %s (%s), %s (%s), %s" % (attr, x, x.__class__, y, y.__class__, test_change(x, y))
				if attr[0] != '_' and attr != 'id' and attr != 'for_update' and test_change(x, y):
					#print "Class is", str(getattr(self, attr).__class__)
					if str(getattr(self, attr).__class__) == "<class 'django.db.models.fields.files.ImageFieldFile'>" or str(getattr(self, attr).__class__) == "<class 'django.db.models.fields.files.FieldFile'>":
						try:
							img = getattr(self, attr)
							img.file.seek(0)
							img.save(img.name, img, False)
							y = img.name
						except:
							pass
					#print "Tracking", x, "to", y
					# See if this change exists
					if c:
						c.data = y
					else:
						c = Change(app_name=app_name, model=myclass.__name__, field=attr, key=self.pk, data=y)
					c.save()
	
	def delete(self, preview=True):
		# Save function for holding changes for approval
		if not preview:
			# Changes can be committed immediately
			super(Model, self).delete()
		else:
			# The CMS needs to track the change
			myclass = self.__class__
			old = myclass.all_objects.get(pk=self.pk)
			old.for_update = 1
			super(Model, old).save()


class TestModel(Model, models.Model):
	"""
	This model is for testing the content management superclass Model above.
	
	>>> from smgsite.cms.models import TestModel
	>>> from smgsite.cms.models import Change
	>>> from smgsite.cms.models import add, delete, change
	>>> x = TestModel(testa=5, testb='char')
	>>> x.save(preview=False)
	>>> x.testb
	'char'
	>>> x.testb = 'newchar'
	>>> x.save()
	>>> y = TestModel.objects.get(testa=5)
	Traceback (most recent call last):
		...
	DoesNotExist: TestModel matching query does not exist.
	>>> y = TestModel.all_objects.get(testa=5)
	>>> x.id == y.id
	True
	>>> y.testb
	u'char'
	>>> obj = Change.objects.get(app_name='cms', model='TestModel', field='testb')
	>>> change(obj.id)
	>>> y = TestModel.all_objects.filter(testa=5)
	>>> y[0].testb
	u'newchar'
	>>> x.delete(preview=False)
	>>> y = TestModel.all_objects.filter(testa=5)
	>>> y
	[]
	>>> x = TestModel(testa=6, testb='char')
	>>> x.save()
	>>> y = TestModel.objects.filter(testa=6)
	>>> y
	[]
	>>> y = TestModel.all_objects.filter(testa=6)
	>>> y[0].for_update
	2
	>>> add('cms', 'TestModel', x.pk)
	>>> y = TestModel.objects.filter(testa=6)
	>>> y
	[<TestModel: TestModel object>]
	>>> x.delete()
	>>> y = TestModel.objects.filter(testa=6)
	>>> y[0].for_update
	1
	>>> delete('cms', 'TestModel', x.pk)
	>>> y = TestModel.objects.filter(testa=6)
	>>> y
	[]
	"""
	
	qa_objects = QAManager()	
	objects = Manager()
	all_objects = models.Manager()
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.BooleanField(default=True)
	testa = models.IntegerField()
	testb = models.CharField(max_length=25)


class ChangeDisplay(object):
	def __init__(self, instance, modelname, name, field, old_data, old_display, new_data, new_display, url, pk):
		self.instance = instance
		self.modelname = modelname
		self.name = name
		self.field = field
		self.old_data = old_data
		self.old_display = old_display
		self.new_data = new_data
		self.new_display = new_display
		self.url = url
		self.pk = pk
	
	def urlupdate(self):
		return self.field == 'urlname' and self.old_data
	
	def postingupdate(self):
		return self.field == 'posting_time' and self.old_data
	
	def eventupdate(self):
		return self.modelname == 'Event' and self.field == 'notification'
	
	def display_old(self):
		if self.field == 'active':
			if self.old_data == '0':
				return 'inactive'
			else:
				return 'active'
		return self.old_display
	
	def display_new(self):
		if self.field == 'active':
			if self.new_data == '0':
				return 'inactive'
			else:
				return 'active'
		return self.new_display


class AdditionDisplay(object):
	def __init__(self, app_name, model, name, url, pk):
		self.app_name = app_name
		self.model = model
		self.name = name
		self.url = url
		self.pk = pk


class ClonableMixin(object):
	def clone(self):
		"""Return an identical copy of the instance with a new ID."""
		if not self.pk:
			raise ValueError('Instance must be saved before it can be cloned.')
		duplicate = copy.copy(self)
		# Setting pk to None tricks Django into thinking this is a new object.
		duplicate.pk = None
		duplicate.urlname = 'COPY: MUST CHANGE'
		duplicate.for_update = 2
		for i in range(10):
			try:
				duplicate.save()
				break
			except IntegrityError:
				duplicate.urlname = 'COPY #%s: MUST CHANGE' % (i)
		# ... but the trick loses all ManyToMany relations.
		for field in self._meta.many_to_many:
			source = getattr(self, field.attname)
			destination = getattr(duplicate, field.attname)
			for item in source.all():
				destination.add(item)
		return duplicate


def find_objects():
	"""
	Method to find all objects pending approval and update
	through the CMS system.
	"""
	
	# Iterate through all applications and all models
	additions = []
	deletions = []
	for app in models.get_apps():
		model_list = models.get_models(app)
		if not model_list:
			continue
		for model in model_list:
			if Model in model.__mro__:
				app_name = model.__module__.split('.')[1]
				# This model is under CMS control
				# Iterate through all instances of the model and construct the items for approval
				try:
					for item in model.all_objects.filter(for_update__gt=0):
						try:
							url = item.get_absolute_url()
						except AttributeError:
							try:
								parent = getattr(item, item.parent)
								url = parent.get_absolute_url()
							except AttributeError:
								url = ''
						if item.for_update == 2:
							additions.append(AdditionDisplay(app_name, model.__name__, str(item), url, item.pk))
						else:
							deletions.append(AdditionDisplay(app_name, model.__name__, str(item), url, item.pk))
				except ObjectDoesNotExist:
					pass
	# Selected changes from the database
	changes = []
	for change in Change.objects.all():
		model = models.get_model(change.app_name, change.model)
		original = model.all_objects.get(pk=change.key)
		try:
			url = original.get_absolute_url()
		except AttributeError:
			url = None
		try:
			old_display = getattr(original, 'cms_%s_display' % change.field)(getattr(original, change.field))
			print "Old display is %s" % old_display
			new_display = getattr(original, 'cms_%s_display' % change.field)(change.data)
		except AttributeError:
			old_display = getattr(original, change.field)
			new_display = change.data
		changes.append(ChangeDisplay(original, change.model, unicode(original), change.field, getattr(original, change.field), old_display, change.data, new_display, url, change.pk))
	return (additions, deletions, changes)


def change(pk):
	try:
		change = Change.objects.get(pk=pk)
		model = models.get_model(change.app_name, change.model)
		original = model.all_objects.get(pk=change.key)
		if change.field == 'active':
			if change.data == '1':
				change.data = ACTIVE
			else:
				change.data = INACTIVE
		setattr(original, change.field, change.data)
		original.save(preview=False)
		change.delete()
	except Change.DoesNotExist:
		pass


def unchange(pk):
	try:
		change = Change.objects.get(pk=pk)
		change.delete()
	except Change.DoesNotExist:
		pass


def add(app, model, pk):
	model = models.get_model(app, model)
	i = model.all_objects.get(pk=pk)
	i.for_update = 0
	i.save(preview=False)


def delete(app, model, pk):
	model = models.get_model(app, model)
	i = model.all_objects.get(pk=pk)
	i.delete(preview=False)


def isValidMarkup(field_data, all_data):
	#field_data = field_data.replace('src="/media', 'src="{{ MEDIA _URL }}')
	#field_data = field_data.replace('href="/media', 'href="{{ MEDIA _URL }}')
	print "Validating markup", field_data
