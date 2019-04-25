# Generated by Django 2.1.7 on 2019-03-14 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190221_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location_off_campus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='location_url_embed',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
    ]