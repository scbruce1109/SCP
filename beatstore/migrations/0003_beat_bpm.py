# Generated by Django 2.2.2 on 2019-07-01 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatstore', '0002_beat_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='beat',
            name='bpm',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
