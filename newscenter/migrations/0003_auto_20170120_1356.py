# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0002_auto_20170120_1355'),
    ]
    
    if 'cms' in settings.INSTALLED_APPS:
        dependencies += [
            ('cms', '0012_auto_20150607_2207'),
        ]

        operations = [
            migrations.CreateModel(
                name='NewsFeedPluginModel',
                fields=[
                    ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='newscenter_newsfeedpluginmodel', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                    ('limit', models.IntegerField(default=5, help_text=b'Maximum number of articles to display', verbose_name=b'Article Limit')),
                    ('location', models.ForeignKey(to='newscenter.Feed')),
                ],
                options={
                    'abstract': False,
                },
                bases=('cms.cmsplugin',),
            ),
        ]
    else:
        operations = []
