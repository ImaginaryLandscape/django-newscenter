# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(unique_for_date=b'release_date', blank=True, help_text=b'Automatically generated from the title.', unique=True, verbose_name=b'ID'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
