# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('newscenter_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('newscenter', ['Feed'])

        # Adding model 'NewsFeedPluginModel'
        db.create_table('newscenter_newsfeedpluginmodel', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], primary_key=True, unique=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newscenter.Feed'])),
            ('limit', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('newscenter', ['NewsFeedPluginModel'])

        # Deleting field 'Newsroom.website_short_name'
        db.delete_column('newscenter_newsroom', 'website_short_name')

        # Adding M2M table for field feeds on 'Article'
        m2m_table_name = db.shorten_name('newscenter_article_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['newscenter.article'], null=False)),
            ('feed', models.ForeignKey(orm['newscenter.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'feed_id'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('newscenter_feed')

        # Deleting model 'NewsFeedPluginModel'
        db.delete_table('newscenter_newsfeedpluginmodel')

        # Adding field 'Newsroom.website_short_name'
        db.add_column('newscenter_newsroom', 'website_short_name',
                      self.gf('django.db.models.fields.SlugField')(blank=True, default='', max_length=64),
                      keep_default=False)

        # Removing M2M table for field feeds on 'Article'
        db.delete_table(db.shorten_name('newscenter_article_feeds'))


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'})
        },
        'newscenter.article': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['newscenter.Category']", 'related_name': "'articles'", 'symmetrical': 'False', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['newscenter.Contact']", 'symmetrical': 'False', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['newscenter.Feed']", 'related_name': "'articles'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newscenter.Location']", 'null': 'True', 'blank': 'True'}),
            'newsroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newscenter.Newsroom']", 'related_name': "'articles'", 'default': '1'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'newscenter.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'newscenter.contact': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'})
        },
        'newscenter.feed': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Feed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'newscenter.image': {
            'Meta': {'ordering': "('sort',)", 'object_name': 'Image'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newscenter.Article']", 'related_name': "'images'"}),
            'caption': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbnail': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'newscenter.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'newscenter.newsfeedpluginmodel': {
            'Meta': {'object_name': 'NewsFeedPluginModel', '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'unique': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newscenter.Feed']"})
        },
        'newscenter.newsroom': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Newsroom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['newscenter']