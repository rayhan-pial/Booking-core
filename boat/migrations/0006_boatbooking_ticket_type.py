# Generated by Django 4.1.1 on 2024-01-07 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0005_boatbooking_confirm_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='boatbooking',
            name='ticket_type',
            field=models.IntegerField(default=0),
        ),
    ]
