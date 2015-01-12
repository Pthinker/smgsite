# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table(u'pages_template', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'pages', ['Template'])

        # Adding model 'Directory'
        db.create_table(u'pages_directory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('directory', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Template'])),
        ))
        db.send_create_signal(u'pages', ['Directory'])

        # Adding model 'Page'
        db.create_table(u'pages_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Directory'])),
            ('urlname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('marketing_banner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pages_marketing_banner', null=True, to=orm['marketing_banners.MarketingBanner'])),
        ))
        db.send_create_signal(u'pages', ['Page'])


    def backwards(self, orm):
        # Deleting model 'Template'
        db.delete_table(u'pages_template')

        # Deleting model 'Directory'
        db.delete_table(u'pages_directory')

        # Deleting model 'Page'
        db.delete_table(u'pages_page')


    models = {
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
        u'pages.directory': {
            'Meta': {'ordering': "['directory']", 'object_name': 'Directory'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Template']"})
        },
        u'pages.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Directory']"}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'marketing_banner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages_marketing_banner'", 'null': 'True', 'to': u"orm['marketing_banners.MarketingBanner']"}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'urlname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pages.template': {
            'Meta': {'object_name': 'Template'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pages']