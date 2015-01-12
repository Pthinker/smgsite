from datetime import date, datetime, timedelta
import smtplib
import os, sys
curdir, curfile = os.path.split(os.path.abspath(__file__))
curdir = os.path.normpath(os.path.join(curdir, '..', '..'))
sys.path.append(curdir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smgsite.settings")
from django.conf import settings

from smgsite.events.models import Registration, Eventtime

def send_confirmations():
	accounts = Registration.objects.filter(status='N')
	for account in accounts:
		toaddrs  = (account.email,)
		fromaddr = 'events@summitmedicalgroup.com'
		msg = 'From: \'Summit Medical Group Event Hotline\' <events@summitmedicalgroup.com>\r\n'
		msg = 'Reply-To: \'Summit Medical Group Event Hotline\' <events@smgnj.com>\r\n'
		msg += 'To: %s\r\n' % account.email
		msg += 'Subject: Thank you for registering\r\n\r\n'
		msg += 'Dear %s %s: \r\n\r\n' % (account.first_name, account.last_name)
		msg += 'You have successfully registered for the following Summit Medical Group events:\r\n\r\n'
		for eventtime in account.eventtimes.filter(active=u'1'):
			msg += '\t* %s (%s)\r\n\r\n' % (eventtime.event.title, eventtime.timelong())
		msg += 'You will receive a reminder approximately 48 hours before each event takes place. If you need to cancel, please reply to this e-mail (events@smgnj.com) or call our Events Hotline at 908-277-8889.\r\n\r\n'
		msg += 'If there are any changes to the program or cancellations, we will notify you using the contact details you provided.\r\n\r\n'
                msg += 'Note: All Lectures are held at Summit Medical Group Conference Center, 1 Diamond Hill Rd, Berkeley Heights, NJ 07922. Please enter through the Lawrence Pavilion Main Entrance by Parking Lot 1.\r\n\r\n'
		msg += 'Thank you,\r\n'
		msg += 'Summit Medical Group\r\n\r\n'

		try:
			server = smtplib.SMTP('localhost')
			server.set_debuglevel(1)
			server.sendmail(fromaddr, toaddrs, msg)
			server.quit()
			account.status = 'C'
			account.save()
		except:
			print 'Unable to send messages to %s because %s' % (toaddrs, sys.exc_info()[0])

def send_reminders():
	for eventtime in Eventtime.objects.filter(startdate__gt=datetime.now() + timedelta(1)).filter(startdate__lte=datetime.now() + timedelta(2)):
		for account in eventtime.registration_set.all():
			toaddrs  = (account.email,)
			fromaddr = 'events@summitmedicalgroup.com'
			msg = 'From: \'Summit Medical Group Event Hotline\' <events@summitmedicalgroup.com>\r\n'
			msg = 'Reply-To: \'Summit Medical Group Event Hotline\' <events@smgnj.com>\r\n'
			msg += 'To: %s\r\n' % account.email
			msg += 'Subject: %s Reminder\r\n\r\n' % eventtime.event.get_event_type_display()
			msg += 'Dear %s %s: \r\n\r\n' % (account.first_name, account.last_name)
			msg += 'This e-mail is to remind you that the %s: "%s" will be taking place on %s' % (eventtime.event.get_event_type_display(), eventtime.event.title, eventtime.startdate.strftime('%a, %b %d, %Y'))
			if eventtime.starttime:
				msg += ' at %s ' % eventtime.starttime.strftime('%I:%M %p')
			else:
				smg += ' '
			msg += 'and will be held at '
			if eventtime.event.location:
				if eventtime.event.location.display_name:
					msg += '%s, ' % eventtime.event.location.display_name
				msg += '%s, ' % eventtime.event.location.address
				if eventtime.event.location.address2:
					msg += '%s, ' % eventtime.event.location.address2
				msg += '%s, %s, %s. ' % (eventtime.event.location.city, eventtime.event.location.state, eventtime.event.room)
			else:
				msg += ' %s. ' % eventtime.event.other_location
			msg += 'For driving directions to Summit Medical Group locations, please visit: http://www.summitmedicalgroup.com/locations/.\r\n\r\n'
			msg += 'If you need to cancel, please reply to this e-mail (events@smgnj.com) or call our Events Hotline at 908-277-8889.\r\n\r\n'
			msg += 'We look forward to seeing you.\r\n'
			msg += 'Summit Medical Group\r\n\r\n'
			try:
				server = smtplib.SMTP('localhost')
				server.set_debuglevel(1)
				server.sendmail(fromaddr, toaddrs, msg.encode('utf-8'))
				server.quit()
				account.status = 'R'
				account.save()
			except:
				print 'Unable to send messages to %s because %s' % (toaddrs, sys.exc_info()[0])


if 'confirmation' in sys.argv:
	print 'Sending confirmations....'
	send_confirmations()
if 'reminder' in sys.argv:
	print 'Sending reminders....'
	send_reminders()
