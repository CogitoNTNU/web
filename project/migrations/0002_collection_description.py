# Generated by Django 2.0.5 on 2018-12-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]