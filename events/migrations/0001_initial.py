# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'], null=True, blank=True)),
            ('other_presenter', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('presenter_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('sponsored_by', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('sponsor_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(default=18, to=orm['site.Location'], null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(default='Conference Center', max_length=100, blank=True)),
            ('other_location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('exclude_from_registration', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('notification', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field related_services on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_related_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('service', models.ForeignKey(orm[u'services.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'service_id'])

        # Adding M2M table for field local_presenters on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_local_presenters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'doctor_id'])

        # Adding model 'Referrer'
        db.create_table(u'events_referrer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal(u'events', ['Referrer'])

        # Adding model 'Registration'
        db.create_table(u'events_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('entered_by', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NJ', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('main_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('alt_phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('referrer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Referrer'])),
            ('sendmail', self.gf('django.db.models.fields.CharField')(default='T', max_length=1)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
        ))
        db.send_create_signal(u'events', ['Registration'])

        # Adding M2M table for field eventtimes on 'Registration'
        m2m_table_name = db.shorten_name(u'events_registration_eventtimes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registration', models.ForeignKey(orm[u'events.registration'], null=False)),
            ('eventtime', models.ForeignKey(orm[u'events.eventtime'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registration_id', 'eventtime_id'])

        # Adding model 'EventBanner'
        db.create_table(u'events_eventbanner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'], null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['EventBanner'])

        # Adding model 'Class'
        db.create_table(u'events_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('starttime', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('enddate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endtime', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('cancellations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('days', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('monday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('tuesday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('wednesday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('thursday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('friday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('saturday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('sunday', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'], null=True, blank=True)),
            ('other_presenter', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('presenter_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('sponsored_by', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('sponsor_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(default=18, to=orm['site.Location'], null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(default='Conference Center', max_length=100, blank=True)),
            ('other_location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Class'])

        # Adding M2M table for field related_services on 'Class'
        m2m_table_name = db.shorten_name(u'events_class_related_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'events.class'], null=False)),
            ('service', models.ForeignKey(orm[u'services.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'service_id'])

        # Adding M2M table for field local_presenters on 'Class'
        m2m_table_name = db.shorten_name(u'events_class_local_presenters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'events.class'], null=False)),
            ('doctor', models.ForeignKey(orm[u'doctors.doctor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'doctor_id'])

        # Adding model 'Eventtime'
        db.create_table(u'events_eventtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('starttime', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('endtime', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('cancelled', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
        ))
        db.send_create_signal(u'events', ['Eventtime'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field related_services on 'Event'
        db.delete_table(db.shorten_name(u'events_event_related_services'))

        # Removing M2M table for field local_presenters on 'Event'
        db.delete_table(db.shorten_name(u'events_event_local_presenters'))

        # Deleting model 'Referrer'
        db.delete_table(u'events_referrer')

        # Deleting model 'Registration'
        db.delete_table(u'events_registration')

        # Removing M2M table for field eventtimes on 'Registration'
        db.delete_table(db.shorten_name(u'events_registration_eventtimes'))

        # Deleting model 'EventBanner'
        db.delete_table(u'events_eventbanner')

        # Deleting model 'Class'
        db.delete_table(u'events_class')

        # Removing M2M table for field related_services on 'Class'
        db.delete_table(db.shorten_name(u'events_class_related_services'))

        # Removing M2M table for field local_presenters on 'Class'
        db.delete_table(db.shorten_name(u'events_class_local_presenters'))

        # Deleting model 'Eventtime'
        db.delete_table(u'events_eventtime')


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
        u'doctors.specialty': {
            'Meta': {'ordering': "['specialty']", 'object_name': 'Specialty'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specialty': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'events.class': {
            'Meta': {'ordering': "['-startdate', '-starttime']", 'object_name': 'Class'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'cancellations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'friday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'local_presenters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['doctors.Doctor']", 'symmetrical': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '18', 'to': u"orm['site.Location']", 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'monday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'other_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'other_presenter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presenter_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'related_services': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'class_s_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['services.Service']"}),
            'room': ('django.db.models.fields.CharField', [], {'default': "'Conference Center'", 'max_length': '100', 'blank': 'True'}),
            'saturday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sponsor_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'sponsored_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'starttime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sunday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'thursday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tuesday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'wednesday': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'})
        },
        u'events.event': {
            'Meta': {'ordering': "['title']", 'object_name': 'Event'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'exclude_from_registration': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'local_presenters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['doctors.Doctor']", 'symmetrical': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '18', 'to': u"orm['site.Location']", 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notification': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'other_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'other_presenter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presenter_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'related_services': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'s_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['services.Service']"}),
            'room': ('django.db.models.fields.CharField', [], {'default': "'Conference Center'", 'max_length': '100', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sponsor_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'sponsored_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'events.eventbanner': {
            'Meta': {'object_name': 'EventBanner'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'events.eventtime': {
            'Meta': {'object_name': 'Eventtime'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'cancelled': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'endtime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'starttime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'events.referrer': {
            'Meta': {'object_name': 'Referrer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'events.registration': {
            'Meta': {'object_name': 'Registration'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'entered_by': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'eventtimes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Eventtime']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'main_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'referrer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Referrer']"}),
            'sendmail': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NJ'", 'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
        }
    }

    complete_apps = ['events']