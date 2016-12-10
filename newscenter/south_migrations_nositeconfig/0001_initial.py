# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('newscenter_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('newscenter', ['Category'])

        # Adding model 'Newsroom'
        db.create_table('newscenter_newsroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('newscenter', ['Newsroom'])

        # Adding model 'Location'
        db.create_table('newscenter_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('newscenter', ['Location'])

        # Adding model 'Article'
        db.create_table('newscenter_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newscenter.Location'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expire_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('newsroom', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='articles', null=True, blank=True, to=orm['newscenter.Newsroom'])),
        ))
        db.send_create_signal('newscenter', ['Article'])

        # Adding M2M table for field categories on 'Article'
        db.create_table('newscenter_article_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['newscenter.article'], null=False)),
            ('category', models.ForeignKey(orm['newscenter.category'], null=False))
        ))
        db.create_unique('newscenter_article_categories', ['article_id', 'category_id'])

        # Adding model 'Image'
        db.create_table('newscenter_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['newscenter.Article'])),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('newscenter', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('newscenter_category')

        # Deleting model 'Newsroom'
        db.delete_table('newscenter_newsroom')

        # Deleting model 'Location'
        db.delete_table('newscenter_location')

        # Deleting model 'Article'
        db.delete_table('newscenter_article')

        # Removing M2M table for field categories on 'Article'
        db.delete_table('newscenter_article_categories')

        # Deleting model 'Image'
        db.delete_table('newscenter_image')


    models = {
        'newscenter.article': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['newscenter.Category']"}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newscenter.Location']", 'null': 'True', 'blank': 'True'}),
            'newsroom': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'articles'", 'null': 'True', 'blank': 'True', 'to': "orm['newscenter.Newsroom']"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'newscenter.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'newscenter.image': {
            'Meta': {'ordering': "('sort',)", 'object_name': 'Image'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['newscenter.Article']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbnail': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'newscenter.location': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'newscenter.newsroom': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Newsroom'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['newscenter']