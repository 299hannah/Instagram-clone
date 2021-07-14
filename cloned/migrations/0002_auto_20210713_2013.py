# Generated by Django 3.2.5 on 2021-07-13 17:13

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloned', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='url',
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]