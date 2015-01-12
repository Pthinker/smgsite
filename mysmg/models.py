import md5
from django.db import models
from smgsite.doctors.models import Doctor
from smgsite.services.models import Service

class User(models.Model):
	"""
	Model for external users.
	"""
	
	active = models.BooleanField()
	
	username = models.EmailField(unique=True)
	password = models.CharField(max_length=32, help_text="This field displays the secure MD5 hash of the user's password. Enter a new password to change this user's password.")
	new_password = models.CharField(max_length=32)
	
	first_name = models.CharField(max_length=25, blank=True)
	middle_name = models.CharField(max_length=25, blank=True)
	last_name = models.CharField(max_length=25, blank=True)
	phone = models.CharField(max_length=19, blank=True)
	zipcode = models.CharField(max_length=5, blank=True)
	
	security_question = models.CharField(max_length=50, blank=True)
	security_answer = models.CharField(max_length=50, blank=True)
	
	confkey = models.CharField(max_length=6)
	
	contact = models.CharField(max_length=1, default=u'0')
	
	def save(self, newpass=False):
		# The save method is overwritten to enable password updates
		try:
			copy = User.objects.get(username=self.username)
			if self.password != copy.password and not newpass:
				self.password = md5.new(self.password).hexdigest()
		except User.DoesNotExist:
			pass
		super(User, self).save()
	
	def fullname(self):
		return u'%s, %s %s' % (self.last_name, self.first_name, self.middle_name)
	
	def display_name(self):
		if self.first_name:
			return u'%s' % (self.first_name)
		else:
			return u'%s' % (self.username)
	
	def __unicode__(self):
		return self.fullname()


class Link(models.Model):
	"""
	Wrapper class to create an array of URLFields
	"""
	title = models.CharField(max_length=200)
	url = models.URLField()


class UserProfile(models.Model):
	"""
	Model for user profiles and MySMG links.	
	"""
	
	user = models.ForeignKey(User, unique=True)
	
	my_doctors = models.ManyToManyField(Doctor)
	my_services = models.ManyToManyField(Service)
	my_library = models.ManyToManyField(Link)

