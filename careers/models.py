from django.db import models
from smgsite.settings import MEDIA_URL
import smgsite.cms.models as cms
from smgsite.site.models import Location
from smgsite.services.models import Service


class Career(cms.Model, models.Model):
	"""
	Model for Careers
	
	This is a model for the careers database.
	"""

	qa_objects = cms.QAManager()
	objects = cms.Manager()
	all_objects = models.Manager()
	item_url = 'career'
	
	SHIFT_TYPE = (
		('F', 'Full time'),
		('P', 'Part time'),
		('D', 'Per Diem'),
	)

	SHIFT_TIME = (
		('M', 'Morning'),
		('D', 'Day'),
		('A', 'Afternoon/Evening'),
		('E', 'Evening'),
		('L', 'Late Night'),
		('W', 'Weekend Day'),
                ('F', 'Flexible'),
    )
	
	STATUS = (
		('N', 'New'),
		('H', 'Hold'),
		('O', 'Open'),
	)
	
	BENEFITS = (
		('N', 'No'),
		('Y', 'Yes'),
		)
	
	for_update = models.PositiveSmallIntegerField(default=2, editable=False)
	active = models.CharField(max_length=1, default=u'1', choices=cms.Model.ACTIVE, editable=False)
	job_title = models.CharField(max_length=50, help_text='Enter a title for this job.')
	position_number = models.CharField(max_length=12, blank=True, help_text='Enter an option position number for this job.')
	department = models.CharField(max_length=50, help_text='Enter a department name.')
	service = models.CharField(max_length=50, blank=True, help_text="Enter an optional service/specialty for this job.")
	location = models.ForeignKey(Location, blank=True, null=True, help_text="Select an optional site location at SMG.")
	other_location = models.TextField(blank=True, help_text="If no site location, enter a location here.")
	shift = models.CharField(max_length=50, blank=True, help_text="Enter shift information for this job.")
	shift_type = models.CharField(max_length=1, choices=SHIFT_TYPE, default='F')
	shift_time = models.CharField(max_length=1, choices=SHIFT_TIME, default='A')
	hours = models.CharField(max_length=8, blank=True, help_text="Enter hours for this job (e.g. 40, or 37.5, or per diem).")
	description = models.TextField(help_text="Enter a description for this job.")
	date_posted = models.DateField(help_text="Enter a posting date for this job.")
	status = models.CharField(max_length=1, choices=STATUS, default='O')
	date_added = models.DateField(auto_now_add=True)
	benefits = models.CharField(max_length=1, choices=BENEFITS, default='N')
	requirements = models.TextField(blank=True, help_text="Enter the requirements for this job.")
	
	class Meta:
		ordering = ['date_posted', 'job_title']
	
	def __unicode__(self):
		return self.job_title
	
	def shift_type_str(self):
		d = dict(self.SHIFT_TYPE)
		return u'%s' % d[self.shift_type]
	
	def shift_time_str(self):
		d = dict(self.SHIFT_TIME)
		return u'%s' % d[self.shift_time]
	
	def status_str(self):
		d = dict(self.STATUS)
		return u'%s' % d[self.status]
		
	def get_absolute_url(self):
		return "/%s/%s/" % (self.item_url, self.pk)

