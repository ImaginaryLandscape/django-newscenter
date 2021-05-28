# Generated by Django 2.2 on 2021-05-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newscenter', '0006_newsroom_featured_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ('sort', 'id')},
        ),
        migrations.AddField(
            model_name='article',
            name='exclude_list',
            field=models.BooleanField(default=False, help_text='Exclude this article from list views'),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, help_text='This will be used for the image alt text.', max_length=255, verbose_name='description'),
        ),
    ]