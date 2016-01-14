# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'newscenter_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'newscenter', ['Feed'])
        for a in orm.Location.objects.all():
            b = orm.Feed(id=a.id, name=a.name, slug=a.slug)
            b.save()

        highest_sequence = db.execute('select id from newscenter_feed order by id desc limit 1;')[0][0]
        db.execute('alter sequence newscenter_feed_id_seq restart with %s;' % (highest_sequence + 1))

        # Adding M2M table for field feeds on 'Article'
        m2m_table_name = db.shorten_name(u'newscenter_article_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'newscenter.article'], null=False)),
            ('feed', models.ForeignKey(orm[u'newscenter.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'feed_id'])
        for obj in orm.Article.objects.all():
            if obj.location:
                obj.feeds.add(obj.location.id)
            obj.save()

        # Changing field 'NewsFeedPluginModel.location'
        db.alter_column(u'newscenter_newsfeedpluginmodel', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newscenter.Feed']))

    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'newscenter_feed')

        # Removing M2M table for field feeds on 'Article'
        db.delete_table(db.shorten_name(u'newscenter_article_feeds'))


        # Changing field 'NewsFeedPluginModel.location'
        db.alter_column(u'newscenter_newsfeedpluginmodel', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newscenter.Location']))

    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'newscenter.article': {
            'Meta': {'ordering': "('-release_date',)", 'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['newscenter.Category']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['newscenter.Contact']", 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['newscenter.Feed']"}),
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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'newscenter.feed': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Feed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
        u'newscenter.newsfeedpluginmodel': {
            'Meta': {'object_name': 'NewsFeedPluginModel', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newscenter.Feed']"})
        },
        u'newscenter.newsroom': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Newsroom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site_config.Website']", 'null': 'True', 'blank': 'True'})
        },
        u'site_config.website': {
            'Meta': {'ordering': "[u'short_name']", 'object_name': 'Website'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['newscenter']
