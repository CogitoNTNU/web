# Generated by Django 2.0.5 on 2018-10-15 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-datetime_published',)},
        ),
    ]