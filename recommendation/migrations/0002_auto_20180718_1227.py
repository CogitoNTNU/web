# Generated by Django 2.0.5 on 2018-07-18 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='type',
            new_name='medium',
        ),
    ]
