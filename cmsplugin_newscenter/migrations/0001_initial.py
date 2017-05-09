# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsFeedPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='cmsplugin_newscenter_newsfeedpluginmodel', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('limit', models.IntegerField(default=5, help_text=b'Maximum number of articles to display', verbose_name=b'Article Limit')),
                ('location', models.ForeignKey(to='newscenter.Feed')),
            ],
            options={
                'db_table': 'newscenter_newsfeedpluginmodel',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
