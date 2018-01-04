# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0003_newsroom_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='caption',
            field=models.CharField(help_text=b'Text to be displayed below the image.', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(help_text=b'This will be used for the image alt text.', max_length=255, verbose_name=b'description'),
        ),
    ]
