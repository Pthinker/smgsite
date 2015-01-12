import csv
import re
from datetime import date
from smgsite.careers.models import Career

date_re = re.compile(r'\s*(\d+)/(\d+)/(\d\d\d\d)')
space_re = re.compile(r'\s\s+')

FILE = 'careers/careers.csv'

f = open(FILE, 'r')
csv_reader = csv.reader(f.readlines())
first = True
for row in csv_reader:
	if first:
		first = False
		continue
	department = row[0]
	department = department.title()
	service = row[1]
	service = space_re.sub('', service)
	location = row[2]
	title = row[3]
	position_number = row[4]
	position_number = position_number[0:12]
	shift_time = row[5]
	for pair in Career.SHIFT_TIME:
		if pair[1].startswith(shift_time) or shift_time.startswith(pair[1]):
			shift_time = pair[0]
			break
	shift_type = row[6]
	if shift_type == 'PT':
		shift_type = 'P'
	else:
		shift_type = 'F'
	description = row[7]
	date_posted = row[8]
	try:
		sstatus = row[9]
	except IndexError:
		sstatus = ''
	if sstatus == 'NEW':
		status = 'N'
	elif sstatus == 'HOLD':
		status = 'H'
	else:
		status = 'O'
	print date_posted
	m = date_re.match(date_posted)
	date_posted = date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
	print date_posted
	print position_number
	print "Service", service
	c = Career(department=department, service=service, other_location=location, job_title=title, position_number=position_number, shift_time=shift_time, shift_type=shift_type, description=description, date_posted=date_posted, for_update=0)
	c.save(preview=False)

