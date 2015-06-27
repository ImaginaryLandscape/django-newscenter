# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('site_config', '__first__'),
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('slug', models.SlugField(unique_for_date=b'release_date', help_text=b'Automatically generated from the title.', unique=True, verbose_name=b'ID')),
                ('body', models.TextField(blank=True)),
                ('teaser', models.TextField(help_text=b'A summary preview of the article.', blank=True)),
                ('release_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publication Date')),
                ('expire_date', models.DateTimeField(null=True, verbose_name=b'Expiration Date', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-release_date',),
                'get_latest_by': 'release_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(help_text=b'Automatically generated from the title.')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('phone', models.CharField(max_length=50, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(help_text=b'Images larger than the configured dimensions will be resized', upload_to=b'newscenter_uploads')),
                ('caption', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(help_text=b'This will be used for alt text.', max_length=100, verbose_name=b'description', blank=True)),
                ('thumbnail', models.BooleanField(default=False, help_text=b'To be displayed on article listing pages. If more than one is selected, the thumbnail used will be chosen at random.', verbose_name=b'Use as Thumbnail')),
                ('sort', models.IntegerField(default=0)),
                ('article', models.ForeignKey(related_name='images', to='newscenter.Article')),
            ],
            options={
                'ordering': ('sort',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsFeedPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('limit', models.IntegerField(default=5, help_text=b'Maximum number of articles to display', verbose_name=b'Article Limit')),
                ('location', models.ForeignKey(to='newscenter.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Newsroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('website', models.ForeignKey(blank=True, to='site_config.Website', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(related_name='articles', null=True, to='newscenter.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='contacts',
            field=models.ManyToManyField(to='newscenter.Contact', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='location',
            field=models.ForeignKey(blank=True, to='newscenter.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='newsroom',
            field=models.ForeignKey(related_name='articles', default=1, to='newscenter.Newsroom'),
            preserve_default=True,
        ),
    ]
