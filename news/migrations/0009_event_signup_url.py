# Generated by Django 2.0.5 on 2018-08-30 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_remove_event_signup_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='signup_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]