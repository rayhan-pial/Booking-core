# Generated by Django 4.1.1 on 2024-01-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourbooking',
            name='adult_ticket_type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourbooking',
            name='child_ticket_type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
