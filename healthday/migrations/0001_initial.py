# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'healthday_topic', (
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('topic_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'healthday', ['Topic'])

        # Adding model 'Category'
        db.create_table(u'healthday_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'healthday', ['Category'])

        # Adding M2M table for field topics on 'Category'
        m2m_table_name = db.shorten_name(u'healthday_category_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'healthday.category'], null=False)),
            ('topic', models.ForeignKey(orm[u'healthday.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'topic_id'])

        # Adding model 'Article'
        db.create_table(u'healthday_article', (
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('article_id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('archive_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('news_type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('blurb', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('feature_blurb', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('feature_image', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('attribution', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'healthday', ['Article'])

        # Adding M2M table for field topics on 'Article'
        m2m_table_name = db.shorten_name(u'healthday_article_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'healthday.article'], null=False)),
            ('topic', models.ForeignKey(orm[u'healthday.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'topic_id'])


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table(u'healthday_topic')

        # Deleting model 'Category'
        db.delete_table(u'healthday_category')

        # Removing M2M table for field topics on 'Category'
        db.delete_table(db.shorten_name(u'healthday_category_topics'))

        # Deleting model 'Article'
        db.delete_table(u'healthday_article')

        # Removing M2M table for field topics on 'Article'
        db.delete_table(db.shorten_name(u'healthday_article_topics'))


    models = {
        u'healthday.article': {
            'Meta': {'ordering': "['posting_time']", 'object_name': 'Article'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'archive_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'article_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'blurb': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'feature_blurb': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'feature_image': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'news_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['healthday.Topic']", 'symmetrical': 'False'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'healthday.category': {
            'Meta': {'ordering': "['category']", 'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['healthday.Topic']", 'symmetrical': 'False'})
        },
        u'healthday.topic': {
            'Meta': {'ordering': "['topic_name']", 'object_name': 'Topic'},
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'}),
            'topic_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['healthday']