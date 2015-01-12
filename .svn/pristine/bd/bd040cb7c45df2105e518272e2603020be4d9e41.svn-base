import os
import re
from django.core.files import File
from urllib import quote
from MySQLdb import IntegrityError
from xml.dom.minidom import parse
from smgsite.relayhealth.models import Article, Advisor, Code, Image

"""
Table drop commands for reimport:
DROP TABLE IF EXISTS `relayhealth_advisor`;
DROP TABLE IF EXISTS `relayhealth_article`;
DROP TABLE IF EXISTS `relayhealth_article_codes`;
DROP TABLE IF EXISTS `relayhealth_article_images`;
DROP TABLE IF EXISTS `relayhealth_article_related`;
DROP TABLE IF EXISTS `relayhealth_code`;
DROP TABLE IF EXISTS `relayhealth_image`;
"""

DIRECTORY = '/home/jthayer/RCPE/2012.2/x'
OUTPUT = '/var/www/qa-smg/smgsite/templates/relayhealth'
XSLPROC = '/usr/bin/xsltproc'
XSLT = '/var/www/qa-smg/smgsite/relayhealth/xml_to_html.xsl'
INDEX_XSLT = '/var/www/qa-smg/smgsite/relayhealth/index_to_html.xsl'

advisor_re = re.compile(r'^(.*)\s+200.*$')
advisor_code_re = re.compile(r'^\w+-(\w+)-.*$')
url_re = re.compile(r'^[^_\.]*-(.{2,3}(-|_|\.).*)\.html$')
clean_re = re.compile(r'[,\(\)\']')
unique_re = re.compile(r'^\w+-\w+-(.*)$')

advisors = {'aha': 'adult_health', 'ac': 'adult_care',
			'ma': 'medications', 'pa': 'pediatric_health'}

illustrations = dict()
images = dict()
related = dict()
references = dict()
uniques = dict()

def build_index(dirpath, dirname, urlname):
	infile = '/%s/%s_index.xml' % (dirpath, dirname)
	filename = '%s-index.html' % urlname
	save_name = clean_re.sub('', filename)
	print '%s %s %s >%s/%s' % (XSLPROC, INDEX_XSLT, infile, OUTPUT, save_name)
	os.system('%s %s %s >%s/%s' % (XSLPROC, INDEX_XSLT, infile, OUTPUT, save_name))
	return 'relayhealth/%s' % filename

def find_files():
	for (dirpath, dirnames, filenames) in os.walk(DIRECTORY):
		dirname = dirpath[dirpath.rindex('/')+1:]
		for filename in filenames:
			print "FILENAME", filename
			print "DIRNAME", dirname
			if filename.endswith('.xml') and not filename.endswith('_refs.xml') and not filename.count('_index') and not filename.count('_credits_'):
				print filename
				filepart = filename[0:filename.rfind('_')]
				advisor_code = filename[0:filename.find('_')]
				if advisor_code == 'aha':
					advisor_name = 'Adult Health Advisor'
				elif advisor_code == 'ac':
					advisor_name = 'Adult Care Advisor'
				elif advisor_code == 'ma':
					advisor_name = 'Medications Advisor'
				elif advisor_code == 'pa':
					advisor_name = 'Pediatric Health Advisor'
				print advisor_name, advisor_code
				path = dirpath + "/" + filename
				dom = parse(path)
				
				language = dom.getElementsByTagName('catalog')[0].getAttribute('language')
				if language != 'english':
					continue
				title = dom.getElementsByTagName('title')[0].firstChild.data
				if title.endswith('Brief Version'):
					continue
				#print "On file", path
				article_id = dom.getElementsByTagName('id')[0].firstChild.data
				unique_id = unique_re.match(article_id).group(1)
				# Look for images and related topics files
				if dom.getElementsByTagName('image'):
					images[article_id] = (dirpath, dom.getElementsByTagName('image')[0].getAttribute('src'))
					continue
				try:
					if dom.getElementsByTagName('header')[0].firstChild.data.find('Related Topics') != -1:
						for rel in dom.getElementsByTagName('linkCRS'):
							if rel.firstChild.data != 'Back to main topic':
								topic = article_id[0:article_id.rfind('_')]
								#print "Related is", rel.getAttribute('id')
								try:
									related[topic].append(rel.getAttribute('id'))
								except KeyError:
									related[topic] = [rel.getAttribute('id')]
						continue
				except IndexError:
					pass
				for rel in dom.getElementsByTagName('linkCRS'):
					if rel.firstChild.data == 'Illustration':
						try:
							illustrations[article_id].append(rel.getAttribute('id'))
						except KeyError:
							illustrations[article_id] = [rel.getAttribute('id')]
					elif rel.firstChild.data == 'References':
						references[article_id] = rel.getAttribute('id')
					elif not rel.firstChild.data.startswith('Corresponding'):
						#print "Related is", rel.getAttribute('id')
						try:
							related[article_id].append(rel.getAttribute('id'))
						except KeyError:
							related[article_id] = [rel.getAttribute('id')]
				kd = dict()
				for keyword in dom.getElementsByTagName('keyword'):
					try:
						for word in keyword.firstChild.data.split(' '):
							kd[word] = 1
					except AttributeError:
						pass
				keywords = ' '.join(kd.keys())				
				advisor = dom.getElementsByTagName('advisor')[0].firstChild.data
				last_reviewed = dom.getElementsByTagName('lastReviewed')[0].firstChild.data
				content = dom.getElementsByTagName('content')[0]
				print content.getElementsByTagName('body')[0]
				print content.getElementsByTagName('body')[0].firstChild
				body = content.getElementsByTagName('body')[0].firstChild.data
				publisher = dom.getElementsByTagName('publisher')[0].firstChild.data
				copyright = dom.getElementsByTagName('copyright')[0].firstChild.data
				disclaimer = dom.getElementsByTagName('mckessondisclaimer')[0].firstChild.data
				
				#advisor_name = advisor_re.match(dom.getElementsByTagName('advisor')[0].firstChild.data).group(1)
				try:
					advisor = Advisor.objects.get(name=advisor_name)
				except Advisor.DoesNotExist:
					advisor_code = advisor_code_re.match(article_id).group(1)
					advisor_url = advisors[dirname]
					advisor_index = build_index(dirpath, dirname, advisors[dirname])
					advisor = Advisor(name=advisor_name, urlname=advisor_url, index=advisor_index, code=advisor_code)
					advisor.save()
				
				save_name = clean_re.sub('', '%s.html' % article_id)
				os.system('%s %s %s >%s/%s' % (XSLPROC, XSLT, path, OUTPUT, save_name))
				
				template = clean_re.sub('', 'relayhealth/%s.html' % article_id)
				print "SAVE NAME", save_name
				urlname = advisors[dirname] + '/' + quote(clean_re.sub('', url_re.match(save_name).group(1))).replace('.', '_')
				print "URL %s for save name %s from %s for %s" % (urlname, save_name, path, article_id)
				add = 1
				basename = urlname
				while True:
					try:
						duplicate = False
						if uniques.has_key(unique_id):
							duplicate = True
						a = Article(urlname=urlname, reference=False, advisor=advisor, article_id=article_id, keywords=keywords, template=template, title=title, duplicate=duplicate)
						a.save(post=False)
						uniques[unique_id] = True
						print "Saving", article_id
						break
					except IntegrityError:
						urlname = basename + "_" + str(add)
						print "Augmenting urlname to", urlname
						add += 1
				for code_group in dom.getElementsByTagName('codes'):
					for code in code_group.getElementsByTagName('code'):
						code_type = code_group.getAttribute('type')
						code = code.firstChild.data
						try:
							c = Code.objects.get(code_type=code_type, code=code)
						except Code.DoesNotExist:
							#print code_type, code
							c = Code(code_type=code_type, code=code)
							c.save()
						a.codes.add(c)
				a.save()
			if filename.endswith('.xml') and filename.endswith('_refs.xml'):
				print filename
				filepart = filename[0:filename.rfind('_')]
				advisor_code = filename[0:filename.find('_')]
				if advisor_code == 'aha':
					advisor_name = 'Adult Health Advisor'
				elif advisor_code == 'ac':
					advisor_name = 'Adult Care Advisor'
				elif advisor_code == 'ma':
					advisor_name = 'Medications Advisor'
				elif advisor_code == 'pa':
					advisor_name = 'Pediatric Health Advisor'
				print advisor_name, advisor_code
				path = dirpath + "/" + filename
				dom = parse(path)
				
				language = dom.getElementsByTagName('catalog')[0].getAttribute('language')
				if language != 'english':
					continue
				title = dom.getElementsByTagName('title')[0].firstChild.data
				if title.endswith('Brief Version'):
					continue
				#print "On file", path
				article_id = dom.getElementsByTagName('id')[0].firstChild.data
				unique_id = unique_re.match(article_id).group(1)
				# Look for images and related topics files
				if dom.getElementsByTagName('image'):
					images[article_id] = (dirpath, dom.getElementsByTagName('image')[0].getAttribute('src'))
					continue
				try:
					if dom.getElementsByTagName('header')[0].firstChild.data.find('Related Topics') != -1:
						for rel in dom.getElementsByTagName('linkCRS'):
							if rel.firstChild.data != 'Back to main topic':
								topic = article_id[0:article_id.rfind('_')]
								#print "Related is", rel.getAttribute('id')
								try:
									related[topic].append(rel.getAttribute('id'))
								except KeyError:
									related[topic] = [rel.getAttribute('id')]
						continue
				except IndexError:
					pass
				for rel in dom.getElementsByTagName('linkCRS'):
					if rel.firstChild.data == 'Illustration':
						try:
							illustrations[article_id].append(rel.getAttribute('id'))
						except KeyError:
							illustrations[article_id] = [rel.getAttribute('id')]
					elif rel.firstChild.data == 'References':
						references[article_id] = rel.getAttribute('id')
					elif not rel.firstChild.data.startswith('Corresponding'):
						#print "Related is", rel.getAttribute('id')
						try:
							related[article_id].append(rel.getAttribute('id'))
						except KeyError:
							related[article_id] = [rel.getAttribute('id')]
				kd = dict()
				for keyword in dom.getElementsByTagName('keyword'):
					for word in keyword.firstChild.data.split(' '):
						kd[word] = 1
				keywords = ' '.join(kd.keys())				
				advisor = dom.getElementsByTagName('advisor')[0].firstChild.data
				content = dom.getElementsByTagName('content')[0]
				print content.getElementsByTagName('body')[0]
				print content.getElementsByTagName('body')[0].firstChild
				body = content.getElementsByTagName('body')[0].firstChild.data
				copyright = dom.getElementsByTagName('copyright')[0].firstChild.data
				#advisor_name = advisor_re.match(dom.getElementsByTagName('advisor')[0].firstChild.data).group(1)
				try:
					advisor = Advisor.objects.get(name=advisor_name)
				except Advisor.DoesNotExist:
					advisor_code = advisor_code_re.match(article_id).group(1)
					advisor_url = advisors[dirname]
					advisor_index = build_index(dirpath, dirname, advisors[dirname])
					advisor = Advisor(name=advisor_name, urlname=advisor_url, index=advisor_index, code=advisor_code)
					advisor.save()
				
				save_name = clean_re.sub('', '%s.html' % article_id)
				os.system('%s %s %s >%s/%s' % (XSLPROC, XSLT, path, OUTPUT, save_name))
				
				template = clean_re.sub('', 'relayhealth/%s.html' % article_id)
				print "SAVE NAME", save_name
				urlname = advisors[dirname] + '/' + quote(clean_re.sub('', url_re.match(save_name).group(1))).replace('.', '_')
				print "URL %s for save name %s from %s for %s" % (urlname, save_name, path, article_id)
				add = 1
				basename = urlname
				while True:
					try:
						duplicate = False
						if uniques.has_key(unique_id):
							duplicate = True
						a = Article(urlname=urlname, reference=True, advisor=advisor, article_id=article_id, keywords=keywords, template=template, title=title, duplicate=duplicate)
						a.save(post=False)
						uniques[unique_id] = True
						print "Saving", article_id
						break
					except IntegrityError:
						urlname = basename + "_" + str(add)
						print "Augmenting urlname to", urlname
						add += 1
				for code_group in dom.getElementsByTagName('codes'):
					for code in code_group.getElementsByTagName('code'):
						code_type = code_group.getAttribute('type')
						code = code.firstChild.data
						try:
							c = Code.objects.get(code_type=code_type, code=code)
						except Code.DoesNotExist:
							#print code_type, code
							c = Code(code_type=code_type, code=code)
							c.save()
						a.codes.add(c)
				a.save()
	print "Illustrations"
	for x in illustrations:
		a = Article.objects.get(article_id=x)
		for y in illustrations[x]:
			try:
				(path, image_name) = images[y]
			except KeyError:
				continue
			#print path, image_name
			try:
				image = Image.objects.get(name=image_name)
			except Image.DoesNotExist:
				print "Creating image", image_name
				f = File(open(path + '/' + image_name))
				image = Image(name=image_name)
				#image.save_image_file(image_name, f.read())
				image.image.save(image_name, f)
                                image.save()
			a.images.add(image)
			a.save()
	print "References"
	for x in references:
		try:
			a = Article.objects.get(article_id=x)
			try:
				b = Article.objects.get(article_id=references[x])
				a.references = b
			except Article.DoesNotExist:
				pass
			a.save()
		except Article.DoesNotExist:
			pass

	print "Related"
	for x in related:
		try:
			a = Article.objects.get(article_id=x)
			for y in related[x]:
				#print x, y
				try:
					b = Article.objects.get(article_id=y)
					a.related.add(b)
				except Article.DoesNotExist:
					pass
			a.save()
		except Article.DoesNotExist:
			pass


find_files()
