# Generated by Django 4.1.1 on 2024-01-04 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0003_flight_confirm_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightbooking',
            name='confirm_booking',
            field=models.BooleanField(default=False),
        ),
    ]
