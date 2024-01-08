from decimal import Decimal
from functools import cached_property
import random

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Car(BaseModel):

    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_car")

    # Fields
    car_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="car_image",
                                  null=True, blank=True)
    description = models.TextField()
    car_features = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    car_name = models.CharField(max_length=255)
    car_type = models.JSONField(default=dict, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highlight = models.JSONField(default=dict, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    average_rating = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255)

    def __str__(self):
        return str(self.car_name)

    def get_absolute_url(self):
        return reverse("car_Car_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_Car_update", args=(self.pk,))

    @cached_property
    def get_image_url(self):
        return self.car_image.get_url if self.car_image else None

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Car, self).save(*args, **kwargs)


class CarBooking(BaseModel):

    # Relationships
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, related_name="booking_car")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_car")

    # Fields
    end_date = models.DateTimeField()
    star_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    booking_number = models.IntegerField()
    confirm_booking = models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.car.car_name)

    def get_absolute_url(self):
        return reverse("car_CarBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_CarBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()

        super(CarBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        if not self.car or not self.star_date or not self.end_date or not self.quantity:
            return 0.00

        # Calculate the duration of the booking in days
        duration_days = (self.end_date - self.star_date).days + 1

        # Get the pricing details of the associated car
        car_pricing = self.car.pricing_car.first()

        if not car_pricing:
            return 0.00

        # Calculate the total cost
        base_price = car_pricing.price * duration_days * self.quantity
        # fixed_price = sum(car_pricing.fixed_price.values())
        # extra_price = sum(car_pricing.extra_price.values()) if car_pricing.extra_price else 0.00

        fixed_price = sum(
            Decimal(value) for value in car_pricing.fixed_price.values())
        extra_price = sum(
            Decimal(value) for value in car_pricing.extra_price.values()) if car_pricing.extra_price else Decimal(
            '0.00')

        total_cost = base_price + fixed_price + extra_price

        if self.car.discount > 0:
            discount_amount = (self.car.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class CarDetails(BaseModel):

    # Relationships
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, related_name="details_car")

    # Fields
    gear_shift = models.IntegerField(default=0)
    door = models.PositiveIntegerField(default=1)
    total_passengers = models.IntegerField(default=0)
    baggage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.car.car_name)

    def get_absolute_url(self):
        return reverse("car_CarDetails_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_CarDetails_update", args=(self.pk,))


class CarFAQ(BaseModel):

    # Relationships
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, related_name="faq_car")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return str(self.car.car_name)

    def get_absolute_url(self):
        return reverse("car_CarFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_CarFAQ_update", args=(self.pk,))


class CarPricing(BaseModel):

    # Relationships
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, related_name="pricing_car")

    # Fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fixed_price = models.JSONField(default=dict, blank=True, null=True)
    extra_price = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return str(self.car.car_name)

    def get_absolute_url(self):
        return reverse("car_CarPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_CarPricing_update", args=(self.pk,))


class CarReview(BaseModel):

    # Relationships
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE, related_name="review_car")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_car")

    # Fields
    review = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.car.car_name)

    def get_absolute_url(self):
        return reverse("car_CarReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("car_CarReview_update", args=(self.pk,))


@receiver(post_save, sender=CarReview)
def update_average_rating(sender, instance, **kwargs):
    car = instance.car

    # Calculate the new average rating
    all_reviews = CarReview.objects.filter(car=car)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        car.average_rating = round(average_rating)
    else:
        car.average_rating = 0

    car.save()