# Generated by Django 4.2 on 2025-01-30 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_newscenter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategoryPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin')),
                ('limit', models.IntegerField(default=5, help_text='Maximum number of articles to display', verbose_name='Article Limit')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newscenter.category')),
            ],
            options={
                'db_table': 'newscenter_newscategorypluginmodel',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
