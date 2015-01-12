import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..'))
sys.path.append(curdir)
from django.core.management import setup_environ
import settings
setup_environ(settings)

from smgsite.doctors.models import Doctor

out = open('hospitals.csv', 'w')
for doctor in Doctor.objects.all().order_by('last_name', 'first_name'):
	hospitals = ''
	for hospital in doctor.hospitals.all().order_by('hospital'):
		hospitals += '%s; ' % hospital
	out.write('"%s", "%s"\n' % (doctor.list_name().encode('utf-8'), hospitals.encode('utf-8')))

