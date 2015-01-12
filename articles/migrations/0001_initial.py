# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'URLAlias'
        db.create_table(u'articles_urlalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'articles', ['URLAlias'])

        # Adding model 'Article'
        db.create_table(u'articles_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('byline_link', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].')),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'], null=True, blank=True)),
            ('leader_promo', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('headline_promo', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('reviewed_by', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reviewed_by_link', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('marketing_banner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='articles_marketing_banner', null=True, to=orm['marketing_banners.MarketingBanner'])),
        ))
        db.send_create_signal(u'articles', ['Article'])

        # Adding M2M table for field aliases on 'Article'
        m2m_table_name = db.shorten_name(u'articles_article_aliases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'articles.article'], null=False)),
            ('urlalias', models.ForeignKey(orm[u'articles.urlalias'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'urlalias_id'])

        # Adding model 'Feature'
        db.create_table(u'articles_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('byline_link', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].')),
            ('reviewed_by', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reviewed_by_link', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'articles', ['Feature'])

        # Adding M2M table for field aliases on 'Feature'
        m2m_table_name = db.shorten_name(u'articles_feature_aliases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm[u'articles.feature'], null=False)),
            ('urlalias', models.ForeignKey(orm[u'articles.urlalias'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feature_id', 'urlalias_id'])

        # Adding M2M table for field related_recipes on 'Feature'
        m2m_table_name = db.shorten_name(u'articles_feature_related_recipes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm[u'articles.feature'], null=False)),
            ('recipe', models.ForeignKey(orm[u'articles.recipe'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feature_id', 'recipe_id'])

        # Adding model 'PressRelease'
        db.create_table(u'articles_pressrelease', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')(default='<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].')),
            ('use_boilerplate', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
        ))
        db.send_create_signal(u'articles', ['PressRelease'])

        # Adding M2M table for field aliases on 'PressRelease'
        m2m_table_name = db.shorten_name(u'articles_pressrelease_aliases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pressrelease', models.ForeignKey(orm[u'articles.pressrelease'], null=False)),
            ('urlalias', models.ForeignKey(orm[u'articles.urlalias'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pressrelease_id', 'urlalias_id'])

        # Adding model 'Recipe'
        db.create_table(u'articles_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('urlname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('byline_link', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipe_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('featured', self.gf('django.db.models.fields.CharField')(default=u'0', max_length=1)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='Description', blank=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(default='Ingredients')),
            ('directions', self.gf('django.db.models.fields.TextField')(default='Directions')),
            ('notes', self.gf('django.db.models.fields.TextField')(default='Notes', blank=True)),
            ('reviewed_by', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reviewed_by_link', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('serving_size', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('num_servings', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('calories', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('fat_cals', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('total_fat', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('saturated_fat', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('trans_fat', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('cholesterol', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('sodium', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('total_carbs', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('dietary_fiber', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('sugars', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('protein', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('vit_a', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('vit_c', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('calcium', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('iron', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
        ))
        db.send_create_signal(u'articles', ['Recipe'])

        # Adding M2M table for field aliases on 'Recipe'
        m2m_table_name = db.shorten_name(u'articles_recipe_aliases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'articles.recipe'], null=False)),
            ('urlalias', models.ForeignKey(orm[u'articles.urlalias'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'urlalias_id'])

        # Adding model 'PDF'
        db.create_table(u'articles_pdf', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_update', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('active', self.gf('django.db.models.fields.CharField')(default=u'1', max_length=1)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('posting_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'articles', ['PDF'])


    def backwards(self, orm):
        # Deleting model 'URLAlias'
        db.delete_table(u'articles_urlalias')

        # Deleting model 'Article'
        db.delete_table(u'articles_article')

        # Removing M2M table for field aliases on 'Article'
        db.delete_table(db.shorten_name(u'articles_article_aliases'))

        # Deleting model 'Feature'
        db.delete_table(u'articles_feature')

        # Removing M2M table for field aliases on 'Feature'
        db.delete_table(db.shorten_name(u'articles_feature_aliases'))

        # Removing M2M table for field related_recipes on 'Feature'
        db.delete_table(db.shorten_name(u'articles_feature_related_recipes'))

        # Deleting model 'PressRelease'
        db.delete_table(u'articles_pressrelease')

        # Removing M2M table for field aliases on 'PressRelease'
        db.delete_table(db.shorten_name(u'articles_pressrelease_aliases'))

        # Deleting model 'Recipe'
        db.delete_table(u'articles_recipe')

        # Removing M2M table for field aliases on 'Recipe'
        db.delete_table(db.shorten_name(u'articles_recipe_aliases'))

        # Deleting model 'PDF'
        db.delete_table(u'articles_pdf')


    models = {
        u'articles.article': {
            'Meta': {'ordering': "['-posting_time']", 'object_name': 'Article'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['articles.URLAlias']", 'null': 'True', 'blank': 'True'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'byline_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'"}),
            'display_time': ('django.db.models.fields.DateTimeField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'headline_promo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'leader_promo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'marketing_banner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articles_marketing_banner'", 'null': 'True', 'to': u"orm['marketing_banners.MarketingBanner']"}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'reviewed_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reviewed_by_link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'articles.feature': {
            'Meta': {'ordering': "['-posting_time']", 'object_name': 'Feature'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['articles.URLAlias']", 'null': 'True', 'blank': 'True'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'byline_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'"}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'display_time': ('django.db.models.fields.DateTimeField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'related_recipes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'recipes_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Recipe']"}),
            'reviewed_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reviewed_by_link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'articles.pdf': {
            'Meta': {'ordering': "['-posting_time']", 'object_name': 'PDF'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_time': ('django.db.models.fields.DateTimeField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'articles.pressrelease': {
            'Meta': {'ordering': "['-posting_time']", 'object_name': 'PressRelease'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['articles.URLAlias']", 'null': 'True', 'blank': 'True'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'<br/>[Type story here]<br/><br/><br/><b>More Information</b><br/><br/>For more information on [enter topic] visit [enter link text and create link].'"}),
            'display_time': ('django.db.models.fields.DateTimeField', [], {}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'use_boilerplate': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'})
        },
        u'articles.recipe': {
            'Meta': {'ordering': "['-posting_time']", 'object_name': 'Recipe'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['articles.URLAlias']", 'null': 'True', 'blank': 'True'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'byline_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'calcium': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'calories': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'cholesterol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Description'", 'blank': 'True'}),
            'dietary_fiber': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'default': "'Directions'"}),
            'display_time': ('django.db.models.fields.DateTimeField', [], {}),
            'fat_cals': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'featured': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'default': "'Ingredients'"}),
            'iron': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "'Notes'", 'blank': 'True'}),
            'num_servings': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'posting_time': ('django.db.models.fields.DateTimeField', [], {}),
            'protein': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'recipe_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reviewed_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reviewed_by_link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'saturated_fat': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'serving_size': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'sodium': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'sugars': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_carbs': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'total_fat': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'trans_fat': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'vit_a': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'vit_c': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        u'articles.urlalias': {
            'Meta': {'ordering': "['urlname']", 'object_name': 'URLAlias'},
            'active': ('django.db.models.fields.CharField', [], {'default': "u'1'", 'max_length': '1'}),
            'for_update': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'urlname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
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
        }
    }

    complete_apps = ['articles']