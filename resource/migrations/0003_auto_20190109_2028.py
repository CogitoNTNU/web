# Generated by Django 2.1.5 on 2019-01-09 19:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_resource_starred_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='starred_by',
            field=models.ManyToManyField(blank=True, related_name='starred_resources', to=settings.AUTH_USER_MODEL),
        ),
    ]