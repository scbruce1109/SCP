# Generated by Django 2.2.2 on 2019-07-08 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatstore', '0011_beat_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
