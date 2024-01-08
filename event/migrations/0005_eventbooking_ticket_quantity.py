# Generated by Django 4.1.1 on 2024-01-03 17:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_eventbooking_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbooking',
            name='ticket_quantity',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), default=[], size=None),
            preserve_default=False,
        ),
    ]
