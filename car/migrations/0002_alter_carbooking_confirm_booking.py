# Generated by Django 4.1.1 on 2024-01-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carbooking',
            name='confirm_booking',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
