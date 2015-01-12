
import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..'))
sys.path.append(curdir)
from django.core.management import setup_environ
import settings
setup_environ(settings)

import datetime

from smgsite.events.models import Event, Registration
from smgsite.events.models import Eventtime

for event in Event.all_objects.all():
	newval = Eventtime(for_update=0, active=u'1', event=event, startdate=event.startdate, starttime=event.starttime, enddate=event.enddate, endtime=event.endtime)
	newval.save(preview=False)
	for r in event.registration_set.all():
		r.eventtimes.add(newval)
		r.save()

