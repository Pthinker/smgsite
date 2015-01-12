# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Advisor'
        db.create_table(u'relayhealth_advisor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('index', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
        ))
        db.send_create_signal(u'relayhealth', ['Advisor'])

        # Adding model 'Code'
        db.create_table(u'relayhealth_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'relayhealth', ['Code'])

        # Adding unique constraint on 'Code', fields ['code_type', 'code']
        db.create_unique(u'relayhealth_code', ['code_type', 'code'])

        # Adding model 'Image'
        db.create_table(u'relayhealth_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'relayhealth', ['Image'])

        # Adding model 'Article'
        db.create_table(u'relayhealth_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('reference', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('advisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relayhealth.Advisor'])),
            ('article_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('references', self.gf('django.db.models.fields.related.ForeignKey')(related_name='referencekey', null=True, to=orm['relayhealth.Article'])),
            ('duplicate', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'relayhealth', ['Article'])

        # Adding M2M table for field images on 'Article'
        m2m_table_name = db.shorten_name(u'relayhealth_article_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'relayhealth.article'], null=False)),
            ('image', models.ForeignKey(orm[u'relayhealth.image'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'image_id'])

        # Adding M2M table for field codes on 'Article'
        m2m_table_name = db.shorten_name(u'relayhealth_article_codes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'relayhealth.article'], null=False)),
            ('code', models.ForeignKey(orm[u'relayhealth.code'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'code_id'])

        # Adding M2M table for field related on 'Article'
        m2m_table_name = db.shorten_name(u'relayhealth_article_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_article', models.ForeignKey(orm[u'relayhealth.article'], null=False)),
            ('to_article', models.ForeignKey(orm[u'relayhealth.article'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_article_id', 'to_article_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Code', fields ['code_type', 'code']
        db.delete_unique(u'relayhealth_code', ['code_type', 'code'])

        # Deleting model 'Advisor'
        db.delete_table(u'relayhealth_advisor')

        # Deleting model 'Code'
        db.delete_table(u'relayhealth_code')

        # Deleting model 'Image'
        db.delete_table(u'relayhealth_image')

        # Deleting model 'Article'
        db.delete_table(u'relayhealth_article')

        # Removing M2M table for field images on 'Article'
        db.delete_table(db.shorten_name(u'relayhealth_article_images'))

        # Removing M2M table for field codes on 'Article'
        db.delete_table(db.shorten_name(u'relayhealth_article_codes'))

        # Removing M2M table for field related on 'Article'
        db.delete_table(db.shorten_name(u'relayhealth_article_related'))


    models = {
        u'relayhealth.advisor': {
            'Meta': {'object_name': 'Advisor'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'relayhealth.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'advisor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['relayhealth.Advisor']"}),
            'article_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'codes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['relayhealth.Code']", 'symmetrical': 'False'}),
            'duplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['relayhealth.Image']", 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'reference': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'references': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referencekey'", 'null': 'True', 'to': u"orm['relayhealth.Article']"}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['relayhealth.Article']", 'symmetrical': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'relayhealth.code': {
            'Meta': {'unique_together': "(('code_type', 'code'),)", 'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'code_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'relayhealth.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['relayhealth']