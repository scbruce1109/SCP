# Generated by Django 2.2.2 on 2019-07-15 03:28

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=products.models.upload_product_file_loc)),
                ('free', models.BooleanField(default=False)),
                ('user_required', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
            ],
        ),
    ]
