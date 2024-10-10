# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0003_newsroom_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newsroom',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='featured',
            field=models.BooleanField(default=True),
        ),
    ]
