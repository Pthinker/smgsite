# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceGroupDetail'
        db.create_table(u'services_servicegroupdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('servicegroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServiceGroup'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'services', ['ServiceGroupDetail'])

        # Adding model 'ServiceGroup'
        db.create_table(u'services_servicegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('seo_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('large_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('marketing_banner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='service_group_marketing_banner', null=True, to=orm['marketing_banners.MarketingBanner'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'services', ['ServiceGroup'])


    def backwards(self, orm):
        # Deleting model 'ServiceGroupDetail'
        db.delete_table(u'services_servicegroupdetail')

        # Deleting model 'ServiceGroup'
        db.delete_table(u'services_servicegroup')


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
        u'services.link_body': {
            'Meta': {'ordering': "['position']", 'object_name': 'Link_Body'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_resource_body'", 'to': u"orm['site.Resource']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']"})
        },
        u'services.link_nav': {
            'Meta': {'ordering': "['position']", 'object_name': 'Link_Nav'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_resource_nav'", 'to': u"orm['site.Resource']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']"})
        },
        u'services.location': {
            'Meta': {'object_name': 'Location'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'extra1': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'extra2': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'extra3': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_location'", 'to': u"orm['site.Location']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']"})
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
        u'services.servicegroup': {
            'Meta': {'object_name': 'ServiceGroup'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'marketing_banner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'service_group_marketing_banner'", 'null': 'True', 'to': u"orm['marketing_banners.MarketingBanner']"}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'seo_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['services.Service']", 'through': u"orm['services.ServiceGroupDetail']", 'symmetrical': 'False'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'services.servicegroupdetail': {
            'Meta': {'object_name': 'ServiceGroupDetail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']"}),
            'servicegroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.ServiceGroup']"})
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

    complete_apps = ['services']