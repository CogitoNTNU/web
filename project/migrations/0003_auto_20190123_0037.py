# Generated by Django 2.1.5 on 2019-01-22 23:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20190118_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='collection_applications', to=settings.AUTH_USER_MODEL),
        ),
    ]
