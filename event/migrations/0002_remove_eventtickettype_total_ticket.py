# Generated by Django 4.1.1 on 2024-01-03 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtickettype',
            name='total_ticket',
        ),
    ]
