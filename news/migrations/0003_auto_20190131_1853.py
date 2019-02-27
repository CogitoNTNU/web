# Generated by Django 2.1.2 on 2019-01-31 17:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190119_1720'),
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