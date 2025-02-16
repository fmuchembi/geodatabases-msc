# Generated by Django 5.1.3 on 2025-02-06 09:51

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('name', models.CharField(max_length=254)),
            ],
            options={
                'db_table': 'your_table_name',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Housing',
        ),
    ]
