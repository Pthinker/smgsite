
import re

from smgsite.doctors.models import Doctor, Specialty

doc_re = re.compile(r'"(.*),\s+(.*)",(.*)')
code_re = re.compile(r'(.+),(\d+).*')

docfile = open('doctors.csv')
codefile = open('codes.csv')

doctors = dict()

for l in docfile:
	m = doc_re.match(l)
	if not m:
		print "Unable to match line '%s'" % l
		raise SystemExit
	last = m.group(1)
	first = m.group(2)
	code = m.group(3)
	d = Doctor.all_objects.filter(last_name=last)
	if not d:
		print "Unable to match '%s', '%s' in the system" % (last, first)
		#raise SystemExit
		continue
	if len(d) > 1:
		#raise SystemExit
		d = Doctor.all_objects.filter(last_name=last, first_name=first)
		if not d:
			print "Unable to match '%s', '%s' in the system" % (last, first)
			#raise SystemExit
			continue
	d = d[0]
	if d.first_name.find(first) == -1:
		print "(Warning) Unable to match first name '%s' to '%s' for '%s'" % (first, d.last_name, last)
		#continue
	doctors[code] = d
#raise SystemExit
for l in codefile:
	m = code_re.match(l)
	if m:
		name = m.group(1)
		code = m.group(2)
		specialty = Specialty.all_objects.filter(specialty=name)
		if not specialty:
			specialty = Specialty(for_update=0, active=u'1', specialty=name)
			specialty.save(preview=False, post=True)
		else:
			specialty = specialty[0]
		try:
			doctor = doctors[code]
			doctor.specialties.add(specialty)
		except KeyError:
			print "Unable to match code '%s' to any doctor" % m.group(2)
