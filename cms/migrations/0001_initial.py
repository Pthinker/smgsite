# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Change'
        db.create_table(u'cms_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('key', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('data', self.gf('django.db.models.fields.TextField')(null=True)),
            ('date_changed', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cms', ['Change'])

        # Adding unique constraint on 'Change', fields ['app_name', 'model', 'field', 'key']
        db.create_unique(u'cms_change', ['app_name', 'model', 'field', 'key'])

        # Adding model 'TestModel'
        db.create_table(u'cms_testmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('testa', self.gf('django.db.models.fields.IntegerField')()),
            ('testb', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'cms', ['TestModel'])


    def backwards(self, orm):
        # Removing unique constraint on 'Change', fields ['app_name', 'model', 'field', 'key']
        db.delete_unique(u'cms_change', ['app_name', 'model', 'field', 'key'])

        # Deleting model 'Change'
        db.delete_table(u'cms_change')

        # Deleting model 'TestModel'
        db.delete_table(u'cms_testmodel')


    models = {
        u'cms.change': {
            'Meta': {'unique_together': "(('app_name', 'model', 'field', 'key'),)", 'object_name': 'Change'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_changed': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'cms.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'testa': ('django.db.models.fields.IntegerField', [], {}),
            'testb': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['cms']