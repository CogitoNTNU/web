# Generated by Django 2.1.5 on 2019-01-14 15:06

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='single_page/files/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('base_appearance', models.BooleanField(default=True)),
                ('url', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='feedfile',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='single_page.SinglePage'),
        ),
    ]
