import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..', '..'))
sys.path.append(curdir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smgsite.settings")
from django.conf import settings

from datetime import date
from django.db import transaction
from smgsite.events.models import Event
from smgsite.search import interface as search

@transaction.commit_on_success
def expire_events():
	for event in Event.display_objects.all():
		if event.expired():
			print "Removing from search event", event
			refname = event.__class__.__module__.split('.')[1] + '.' + event.__class__.__name__
			search.delete(refname, event.pk)
			search.delete('Keyword', 'Keyword-' + str(event.pk))

expire_events()
