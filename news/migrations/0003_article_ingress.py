# Generated by Django 2.0.5 on 2018-05-07 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20180507_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='ingress',
            field=models.TextField(blank=True, null=True),
        ),
    ]