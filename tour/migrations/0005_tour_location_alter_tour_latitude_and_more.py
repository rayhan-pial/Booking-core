# Generated by Django 4.1.1 on 2024-01-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0004_tourbooking_confirm_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='location',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tour',
            name='latitude',
            field=models.DecimalField(decimal_places=9, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='tour',
            name='longitude',
            field=models.DecimalField(decimal_places=9, default=0.0, max_digits=12),
        ),
    ]
