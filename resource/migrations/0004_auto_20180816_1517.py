# Generated by Django 2.0.5 on 2018-08-16 13:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('concurrency', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resource', '0003_auto_20180719_1611'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='Resource',
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ('-creation_date',)},
        ),
    ]