# Generated by Django 4.1.1 on 2024-01-01 04:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        ('customer', '0001_initial'),
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('highlight', models.JSONField(blank=True, default=dict, null=True)),
                ('cancellation_policy', models.TextField()),
                ('longitude', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('average_rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('amenities', models.JSONField(blank=True, default=dict, null=True)),
                ('boat_type', models.JSONField(blank=True, default=dict, null=True)),
                ('latitude', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('terms_Information', models.TextField()),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField()),
                ('boat_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('boat_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boat_image', to='coreapp.document')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_boat', to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='BoatTicketType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('total_ticket', models.IntegerField(default=0)),
                ('ticket_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BoatSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('engines', models.CharField(max_length=255)),
                ('year', models.DateField()),
                ('fuel', models.CharField(max_length=255)),
                ('total_crew', models.IntegerField(default=0)),
                ('boat_model', models.CharField(max_length=255)),
                ('boat_skipper', models.CharField(max_length=255)),
                ('boat_manufacturer', models.CharField(max_length=255)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specs_boat', to='boat.boat')),
            ],
        ),
        migrations.CreateModel(
            name='BoatReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('rating', models.IntegerField(default=0)),
                ('review_time', models.DateTimeField()),
                ('review', models.TextField()),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_boat', to='boat.boat')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_review_boat', to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BoatPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('fixed_price', models.JSONField(blank=True, default=dict, null=True)),
                ('extra_price', models.JSONField(blank=True, default=dict, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_boat', to='boat.boat')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_pricing_boat', to='boat.boattickettype')),
            ],
        ),
        migrations.CreateModel(
            name='BoatFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('faq', models.JSONField(blank=True, default=dict, null=True)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faq_boat', to='boat.boat')),
            ],
        ),
        migrations.CreateModel(
            name='BoatDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('length', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('max_guest', models.IntegerField(default=0)),
                ('cabin', models.IntegerField(default=0)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_boat', to='boat.boat')),
            ],
        ),
        migrations.CreateModel(
            name='BoatBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('total_time', models.IntegerField(default=0)),
                ('booking_number', models.IntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('start_time', models.DateTimeField()),
                ('star_date', models.DateTimeField()),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_boat', to='boat.boat')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_booking_boat', to='customer.customer')),
            ],
        ),
    ]
