# Generated by Django 4.1.1 on 2024-01-01 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.SmallIntegerField(choices=[(0, 'Paypal'), (1, 'BillPlz'), (2, 'Cash')]),
        ),
    ]
