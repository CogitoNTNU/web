# Generated by Django 2.0.5 on 2019-01-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190102_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='description',
            field=models.TextField(),
        ),
    ]