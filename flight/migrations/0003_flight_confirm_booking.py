# Generated by Django 4.1.1 on 2024-01-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_remove_flightbooking_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='confirm_booking',
            field=models.BooleanField(default=False),
        ),
    ]
