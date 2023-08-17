# -*- coding: utf-8 -*-

from django.db import migrations, models
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('newscenter', '0004_auto_20170509_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='audio_file',
            field=filer.fields.file.FilerFileField(related_name='article_audio', blank=True, to='filer.File', null=True, on_delete=models.CASCADE),
        ),
    ]
