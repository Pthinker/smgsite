# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'marketing_banners_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('remote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'marketing_banners', ['Resource'])

        # Adding model 'MarketingBanner'
        db.create_table(u'marketing_banners_marketingbanner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marketing_banners.Resource'])),
        ))
        db.send_create_signal(u'marketing_banners', ['MarketingBanner'])

        # Adding model 'MBGroup'
        db.create_table(u'marketing_banners_mbgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('urls', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'marketing_banners', ['MBGroup'])

        # Adding M2M table for field banners on 'MBGroup'
        m2m_table_name = db.shorten_name(u'marketing_banners_mbgroup_banners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mbgroup', models.ForeignKey(orm[u'marketing_banners.mbgroup'], null=False)),
            ('marketingbanner', models.ForeignKey(orm[u'marketing_banners.marketingbanner'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mbgroup_id', 'marketingbanner_id'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'marketing_banners_resource')

        # Deleting model 'MarketingBanner'
        db.delete_table(u'marketing_banners_marketingbanner')

        # Deleting model 'MBGroup'
        db.delete_table(u'marketing_banners_mbgroup')

        # Removing M2M table for field banners on 'MBGroup'
        db.delete_table(db.shorten_name(u'marketing_banners_mbgroup_banners'))


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
        u'marketing_banners.mbgroup': {
            'Meta': {'object_name': 'MBGroup'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'banners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['marketing_banners.MarketingBanner']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'urls': ('django.db.models.fields.TextField', [], {})
        },
        u'marketing_banners.resource': {
            'Meta': {'ordering': "['name']", 'object_name': 'Resource'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'remote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['marketing_banners']