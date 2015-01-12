import MySQLdb
import re
import smgsite.doctors.models as doctors
import smgsite.services.models as services
import smgsite.site.models as site
from smgsite.search import interface
from urllib import urlretrieve
from PIL import Image

specialty_re = re.compile(r'(\s*/\s*|\s+)')
suffix_re = re.compile(r'(.*),\s*(.*)')
phone_re = re.compile(r'.*(\d\d\d).*(\d\d\d).*(\d\d\d\d).*')
cert_re = re.compile(r'\s*([^;]+(; \d+)*)(;|$)')

def replace_photos():
	db = MySQLdb.connect(db='sum136', use_unicode=True, charset="utf8")
	c = db.cursor()
	c.execute("SELECT prefix, fname, initial, lname, accred, phonenum, faxnum, deleted, adddate, id, docnumber FROM doctor WHERE deleted != 'Y'")
	for r in c.fetchall():
		lname = r[3]
		m = suffix_re.match(r[3])
		if m:
			lname = m.group(1)
			suffix = m.group(2)
		url = str(r[1][0] + lname).lower()
		try:
			d = doctors.Doctor.objects.get(first_name=r[1], last_name=r[3])
			photo_url = "http://www.summitmedicalgroup.com/images/doctors/%s.jpg" % (r[10])
			(filename, headers) = urlretrieve(photo_url)
			if headers.type == 'image/jpeg':
				f = open(filename)
				savename = url + ".jpg"
				d.save_original_image_file(savename, f.read())
		except doctors.Doctor.DoesNotExist:
			print "Doctor %s %s does not exist!" % (r[1], r[3])
		except IOError, detail:
			print "Error importing image for", photo_url, detail
		d.save(preview=False)

def initial_import():
	db = MySQLdb.connect(db='sum136', use_unicode=True, charset="utf8")

	c = db.cursor()
	c1 = db.cursor()

	sdb = MySQLdb.connect(db='smgsurvey', use_unicode=True, charset="utf8")

	sc = sdb.cursor()

	c.execute("SELECT Name, locdesc, Add1, Add2, City, State, Zip, Phone, Fax, sortorder, id FROM location WHERE Deleted != 'Y'")

	addresses = dict()

	for r in c.fetchall():
		phone = ''
		if r[7]:
			m = phone_re.match(r[7])
			if m:
				phone = "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
		fax = ''
		if r[8]:
			m = phone_re.match(r[8])
			if m:
				fax = "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
		a2 = ''
		if r[3]:
			a2 = r[3]
		addresses[r[10]] = r[0]

	c.execute("SELECT specialty, specialty_sort, description, deleted, adddate, ParkingDesc FROM specialty LEFT JOIN parking ON (parking.id = specialty.ParkingID) WHERE deleted != 'Y'")

	for r in c.fetchall():
		url = specialty_re.sub('-', r[0].lower())
		active = True
		if r[3] == 'Y':
			active = False
		practitioner_group = "Our " + r[1] + "s"
		s = services.Service(urlname=url, name=r[0], practitioner_name=r[1], practitioner_group=practitioner_group, content=r[2], active=active, date_added=r[4], phone='', for_update=0)
		x = site.Location.objects.filter(parking_name=r[5])
		if len(x) > 0:
			s.location = x[0]
		s.save(preview=False) # The first save generates the primary key
		s.save(preview=False) # Save has to be duplicated for information to be committed to the search engine.

	c.execute("SELECT prefix, fname, initial, lname, accred, phonenum, faxnum, deleted, adddate, id, docnumber FROM doctor WHERE deleted != 'Y'")

	for r in c.fetchall():
		if r[9] == 136:
			continue
		suffix = ''
		m = suffix_re.match(r[3])
		lname = r[3]
		if m:
			lname = m.group(1)
			suffix = m.group(2)
		url = str(r[1][0] + lname).lower()
		email = url + "@smgnj.com"
		letters = r[4].replace('.', '')
		phone = ''
		if (r[5]):
			m = phone_re.match(r[5])
			if m:
				phone = "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
		fax = ''
		if (r[6]):
			m = phone_re.match(r[6])
			if m:
				fax = "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
		active = True
		if r[7] == 'Y':
			active = False
		sc.execute("SELECT interests, decision, philosophy from form_survey WHERE oldid = %s", r[10])
		touch = ''
		try:
			touch = ''.join(sc.fetchone())
		except TypeError:
			pass
		try:
			d = doctors.Doctor(urlname=url, prefix=r[0], first_name=r[1], middle_name=r[2], last_name=r[3], suffix=suffix, letters=letters, email=email, phone=phone, fax=fax, touch=touch, active=active, date_added=r[8], for_update=0)
			c1.execute("SELECT locationid FROM location_relationship WHERE doctorid = %s ORDER BY locationid ASC", r[9])
			try:
				photo_url = "http://www.summitmedicalgroup.com/images/doctors/%s.jpg" % (r[10])
				(filename, headers) = urlretrieve(photo_url)
				if headers.type == 'image/jpeg':
					f = open(filename)
					savename = url + ".jpg"
					d.save_original_image_file(savename, f.read())
			except IOError, detail:
				print "Error importing image for", photo_url, detail
			d.save(preview=False)
			initial = True
			for r1 in c1.fetchall():
				if initial:
					try:
						x = site.Location.objects.filter(name=addresses[r1[0]])
						if len(x) > 0:
							d.location = x[0]
							initial = False
					except KeyError:
						pass
				else:
					try:
						x = site.Location.objects.filter(name=addresses[r1[0]])
						if len(x) > 0:
							d.extra_locations.add(x[0])
					except KeyError:
						pass
			d.save(preview=False)
			c1.execute("SELECT specialty FROM specialty, doctor, specialty_relationship WHERE doctor.id = %s AND specialty.id = specialty_relationship.specialtyID AND doctor.id = specialty_relationship.doctorID AND specialty.deleted != 'Y' ORDER BY specialty_sort ASC", (r[9]),)
			initial = True
			for r1 in c1.fetchall():
				s = services.Service.objects.get(name=r1[0])
				if initial:
					d.title_service = s
					initial = False
				else:
					d.services.add(s)
			d.save(preview=False)
			c1.execute("SELECT type, description FROM accreditation WHERE deleted != 'Y' AND doctorid = %s", (r[9]),)
			for r1 in c1.fetchall():
				if len(r1[0]) == 0: # Don't copy empty accreditations
					continue
				if len(r1[0]) <= 4: # This is a degree
					letters = r1[0].strip(':')
					try:
						degree = doctors.Degree_letters.objects.get(letters=letters)
					except doctors.Degree_letters.DoesNotExist:
						degree = doctors.Degree_letters(letters=letters)
						degree.save()
					a = doctors.Degree(doctor=d, letters=degree, description=r1[1], for_update=0)
					a.save(preview=False)
				else:
					name = r1[0].strip(':')
					description = r1[1]
					if name == 'Board Certifications':
						name = 'Board Certification'
					for item in cert_re.finditer(r1[1]):
						description = item.group(1)
						try:
							accreditation = doctors.Accreditation_name.objects.get(name=name)
						except doctors.Accreditation_name.DoesNotExist:
							accreditation = doctors.Accreditation_name(name=name)
							accreditation.save()
						a = doctors.Accreditation(doctor=d, name=accreditation, description=description, for_update=0)
						a.save(preview=False)
			degree_order = 1
			accreditation_order = 1
			c1.execute("SELECT type, sortorder FROM accred_sort_order ORDER BY sortorder ASC")
			for r1 in c1.fetchall():
				name = r1[0].strip(':')
				try:
					degree = doctors.Degree_letters.objects.get(letters=name)
					degree.sort_order = degree_order
					degree.save()
					degree_order += 1
				except doctors.Degree_letters.DoesNotExist:
					pass
				try:
					accreditation = doctors.Accreditation_name.objects.get(name=name)
					accreditation.sort_order = accreditation_order
					accreditation.save()
					accreditation_order += 1
				except doctors.Accreditation_name.DoesNotExist:
					pass
		except c.IntegrityError, detail:
			print "Integrity error", detail

	interface.optimize()

