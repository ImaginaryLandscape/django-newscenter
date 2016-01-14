# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Article.newsroom'
        db.alter_column(u'newscenter_article', 'newsroom_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newscenter.Newsroom']))
        # Adding field 'Newsroom.website_short_name'
        db.add_column(u'newscenter_newsroom', 'website_short_name',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=64, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Article.newsroom'
        db.alter_column(u'newscenter_article', 'newsroom_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['newscenter.Newsroom']))
        # Deleting field 'Newsroom.website_short_name'
        db.delete_column(u'newscenter_newsroom', 'website_short_name')


    models = {
        u'newscenter.article': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['newscenter.Category']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['newscenter.Contact']", 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newscenter.Location']", 'null': 'True', 'blank': 'True'}),
            'newsroom': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'articles'", 'to': u"orm['newscenter.Newsroom']"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'newscenter.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'newscenter.contact': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'newscenter.image': {
            'Meta': {'ordering': "('sort',)", 'object_name': 'Image'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['newscenter.Article']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbnail': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'newscenter.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'newscenter.newsroom': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Newsroom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'website_short_name': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['newscenter']