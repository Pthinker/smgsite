# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hospital'
        db.create_table(u'doctors_hospital', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hospital', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hospital_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'doctors', ['Hospital'])

        # Adding model 'Language'
        db.create_table(u'doctors_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'doctors', ['Language'])

        # Adding model 'Specialty'
        db.create_table(u'doctors_specialty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('specialty', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'doctors', ['Specialty'])

        # Adding model 'SpecialtyUpdate'
        db.create_table(u'doctors_specialtyupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('specialty', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'doctors', ['SpecialtyUpdate'])

        # Adding model 'Doctor'
        db.create_table(u'doctors_doctor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('seo_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('letters', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('cropped_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('title_service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title_service', null=True, to=orm['services.Service'])),
            ('touch', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('exclude_from_index', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogs.Blog'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('accepting_flag', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('accepting', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('patient_portal', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('appointments', self.gf('django.db.models.fields.CharField')(default=u'P', max_length=1)),
            ('email_doctor', self.gf('django.db.models.fields.CharField')(default=u'P', max_length=1)),
            ('email_staff', self.gf('django.db.models.fields.CharField')(default=u'P', max_length=1)),
            ('lab_results', self.gf('django.db.models.fields.CharField')(default=u'P', max_length=1)),
            ('health_records', self.gf('django.db.models.fields.CharField')(default=u'P', max_length=1)),
            ('marketing_banner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='doctors_marketing_banner', null=True, to=orm['marketing_banners.MarketingBanner'])),
        ))
        db.send_create_signal(u'doctors', ['Doctor'])

        # Adding M2M table for field hospitals on 'Doctor'
        m2m_table_name = db.shorten_name(u'doctors_doctor_hospitals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False)),
            ('hospital', models.ForeignKey(orm[u'doctors.hospital'], null=False))
        ))
        db.create_unique(m2m_table_name, ['doctor_id', 'hospital_id'])

        # Adding M2M table for field languages on 'Doctor'
        m2m_table_name = db.shorten_name(u'doctors_doctor_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False)),
            ('language', models.ForeignKey(orm[u'doctors.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['doctor_id', 'language_id'])

        # Adding M2M table for field services on 'Doctor'
        m2m_table_name = db.shorten_name(u'doctors_doctor_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False)),
            ('service', models.ForeignKey(orm[u'services.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['doctor_id', 'service_id'])

        # Adding M2M table for field specialties on 'Doctor'
        m2m_table_name = db.shorten_name(u'doctors_doctor_specialties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False)),
            ('specialty', models.ForeignKey(orm[u'doctors.specialty'], null=False))
        ))
        db.create_unique(m2m_table_name, ['doctor_id', 'specialty_id'])

        # Adding model 'Degree_letters'
        db.create_table(u'doctors_degree_letters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letters', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('description_short', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description_long', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'doctors', ['Degree_letters'])

        # Adding model 'Degree'
        db.create_table(u'doctors_degree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('letters', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Degree_letters'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'doctors', ['Degree'])

        # Adding model 'Accreditation_name'
        db.create_table(u'doctors_accreditation_name', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name_plural', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'doctors', ['Accreditation_name'])

        # Adding model 'Accreditation'
        db.create_table(u'doctors_accreditation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Accreditation_name'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'doctors', ['Accreditation'])

        # Adding model 'Link_Nav'
        db.create_table(u'doctors_link_nav', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='doctor_resource_nav', to=orm['site.Resource'])),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'doctors', ['Link_Nav'])

        # Adding model 'Featured'
        db.create_table(u'doctors_featured', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'doctors', ['Featured'])

        # Adding model 'Location'
        db.create_table(u'doctors_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='doctors_location', to=orm['site.Location'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('extra1', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('extra2', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('extra3', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal(u'doctors', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Hospital'
        db.delete_table(u'doctors_hospital')

        # Deleting model 'Language'
        db.delete_table(u'doctors_language')

        # Deleting model 'Specialty'
        db.delete_table(u'doctors_specialty')

        # Deleting model 'SpecialtyUpdate'
        db.delete_table(u'doctors_specialtyupdate')

        # Deleting model 'Doctor'
        db.delete_table(u'doctors_doctor')

        # Removing M2M table for field hospitals on 'Doctor'
        db.delete_table(db.shorten_name(u'doctors_doctor_hospitals'))

        # Removing M2M table for field languages on 'Doctor'
        db.delete_table(db.shorten_name(u'doctors_doctor_languages'))

        # Removing M2M table for field services on 'Doctor'
        db.delete_table(db.shorten_name(u'doctors_doctor_services'))

        # Removing M2M table for field specialties on 'Doctor'
        db.delete_table(db.shorten_name(u'doctors_doctor_specialties'))

        # Deleting model 'Degree_letters'
        db.delete_table(u'doctors_degree_letters')

        # Deleting model 'Degree'
        db.delete_table(u'doctors_degree')

        # Deleting model 'Accreditation_name'
        db.delete_table(u'doctors_accreditation_name')

        # Deleting model 'Accreditation'
        db.delete_table(u'doctors_accreditation')

        # Deleting model 'Link_Nav'
        db.delete_table(u'doctors_link_nav')

        # Deleting model 'Featured'
        db.delete_table(u'doctors_featured')

        # Deleting model 'Location'
        db.delete_table(u'doctors_location')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blogs.blog': {
            'Meta': {'ordering': "['name']", 'object_name': 'Blog'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'authors'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editors'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'doctors.accreditation': {
            'Meta': {'object_name': 'Accreditation'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Accreditation_name']"})
        },
        u'doctors.accreditation_name': {
            'Meta': {'object_name': 'Accreditation_name'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_plural': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'doctors.degree': {
            'Meta': {'object_name': 'Degree'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Degree_letters']"})
        },
        u'doctors.degree_letters': {
            'Meta': {'object_name': 'Degree_letters'},
            'description_long': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_short': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'doctors.doctor': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Doctor'},
            'accepting': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'accepting_flag': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'appointments': ('django.db.models.fields.CharField', [], {'default': "u'P'", 'max_length': '1'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.Blog']", 'null': 'True', 'blank': 'True'}),
            'cropped_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'email_doctor': ('django.db.models.fields.CharField', [], {'default': "u'P'", 'max_length': '1'}),
            'email_staff': ('django.db.models.fields.CharField', [], {'default': "u'P'", 'max_length': '1'}),
            'exclude_from_index': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'health_records': ('django.db.models.fields.CharField', [], {'default': "u'P'", 'max_length': '1'}),
            'hospitals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['doctors.Hospital']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'lab_results': ('django.db.models.fields.CharField', [], {'default': "u'P'", 'max_length': '1'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['doctors.Language']", 'symmetrical': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'letters': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'marketing_banner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'doctors_marketing_banner'", 'null': 'True', 'to': u"orm['marketing_banners.MarketingBanner']"}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'patient_portal': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'seo_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'services'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['services.Service']"}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['doctors.Specialty']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title_service'", 'null': 'True', 'to': u"orm['services.Service']"}),
            'touch': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'doctors.featured': {
            'Meta': {'ordering': "['startdate', 'enddate']", 'object_name': 'Featured'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        u'doctors.hospital': {
            'Meta': {'ordering': "['hospital']", 'object_name': 'Hospital'},
            'hospital': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hospital_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'doctors.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'doctors.link_nav': {
            'Meta': {'ordering': "['resource']", 'object_name': 'Link_Nav'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doctor_resource_nav'", 'to': u"orm['site.Resource']"})
        },
        u'doctors.location': {
            'Meta': {'object_name': 'Location'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'extra1': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'extra2': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'extra3': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doctors_location'", 'to': u"orm['site.Location']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'doctors.specialty': {
            'Meta': {'ordering': "['specialty']", 'object_name': 'Specialty'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specialty': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'doctors.specialtyupdate': {
            'Meta': {'ordering': "['specialty']", 'object_name': 'SpecialtyUpdate'},
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specialty': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'marketing_banners.marketingbanner': {
            'Meta': {'object_name': 'MarketingBanner'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['marketing_banners.Resource']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'marketing_banners.resource': {
            'Meta': {'ordering': "['name']", 'object_name': 'Resource'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'services.service': {
            'Meta': {'ordering': "['name']", 'object_name': 'Service'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['services.URLAlias']", 'null': 'True', 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.Blog']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_short': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'learn_more': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'marketing_banner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'services_marketing_banner'", 'null': 'True', 'to': u"orm['marketing_banners.MarketingBanner']"}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'offerings': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'patient_tools': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'practitioner_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'practitioner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'related_services': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'seo_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Template']", 'null': 'True', 'blank': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'services.template': {
            'Meta': {'object_name': 'Template'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'services.urlalias': {
            'Meta': {'ordering': "['urlname']", 'object_name': 'URLAlias'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'site.location': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Location'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'display': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'friday': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'glatitude': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'glongitude': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hours_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'monday': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parking_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'parking_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'starttime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NJ'", 'max_length': '2'}),
            'thursday': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'tuesday': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'wednesday': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'site.resource': {
            'Meta': {'ordering': "['name']", 'object_name': 'Resource'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['doctors']