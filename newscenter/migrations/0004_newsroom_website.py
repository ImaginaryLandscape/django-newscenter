# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0003_auto_20170120_1356'),
    ]
    
    if 'site_config.backends.model_backend' in settings.INSTALLED_APPS:
        dependencies += [
            ('site_config', '__first__'),
        ]

        operations = [
            migrations.AddField(
                model_name='newsroom',
                name='website',
                field=models.ForeignKey(blank=True, to='site_config.Website', null=True),
            ),
        ]
    else:
        operations = []
