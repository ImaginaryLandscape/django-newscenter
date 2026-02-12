# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0004_auto_20170509_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='audio_file',
            field=models.FileField(blank=True, null=True),
        ),
    ]
