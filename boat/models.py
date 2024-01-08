import random
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from django.core.validators import MaxValueValidator
from functools import cached_property
from datetime import datetime, timedelta
from helper import location


class Boat(BaseModel):
    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_boat")

    # Fields
    highlight = models.JSONField(default=dict, blank=True, null=True)
    cancellation_policy = models.TextField()
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    average_rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], default=0)
    amenities = models.JSONField(default=dict, blank=True, null=True)
    boat_type = models.JSONField(default=dict, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    terms_Information = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()
    boat_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    boat_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="boat_image",
                                   null=True, blank=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return str(self.boat_name)

    def get_absolute_url(self):
        return reverse("boat_Boat_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_Boat_update", args=(self.pk,))

    @cached_property
    def get_image_url(self):
        return self.boat_image.get_url if self.boat_image else None

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Boat, self).save(*args, **kwargs)


class BoatBooking(BaseModel):
    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_boat")
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="booking_boat")

    # Fields
    total_time = models.IntegerField(default=0)
    booking_number = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_day = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    star_date = models.DateTimeField()
    end_date = models.DateTimeField()
    confirm_booking = models.BooleanField(default=False)
    ticket_type = models.IntegerField(default=0)

    def __str__(self):
        return str(f"{self.boat.boat_name} {self.total_cost}")

    def get_absolute_url(self):
        return reverse("boat_BoatBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()
        self.end_date = self.calculate_end_date()

        super(BoatBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        if not self.boat or not self.star_date or not self.start_time:
            return 0.00

        if self.total_time > 0:
            # Calculate the duration of the booking in days
            # duration = Decimal(str(self.total_time + self.start_time.hour + self.start_time.minute / 60))
            # timestamp = datetime.strptime(self.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            # time_in_hours = Decimal(str(self.start_time.hour + self.start_time.minute / 60.0))
            # duration = (self.total_time + time_in_hours)
            duration = self.total_time

        elif self.total_day > 0:
            # duration = Decimal(str(self.total_day * 24))
            duration = self.total_day + 1

        # Get the pricing details of the associated
        # boat_pricing = self.boat.pricing_boat.first()
        boat_pricing = self.boat.pricing_boat.get(ticket_type=self.ticket_type)

        if not boat_pricing:
            return 0.00

        # Calculate the total cost
        base_price = boat_pricing.price * duration
        # fixed_price = sum(int(boat_pricing.fixed_price.values())) if boat_pricing.fixed_price else 0.00
        # extra_price = sum(int(boat_pricing.extra_price.values())) if boat_pricing.extra_price else 0.00
        fixed_price = sum(
            int(value) for value in boat_pricing.fixed_price.values()) if boat_pricing.fixed_price else 0.00
        extra_price = sum(
            int(value) for value in boat_pricing.extra_price.values()) if boat_pricing.extra_price else 0.00

        total_cost = base_price + fixed_price + extra_price

        if self.boat.discount > 0:
            discount_amount = (self.boat.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost

    def calculate_end_date(self):
        if self.total_time > 0:
            # total_hours = self.total_time + self.start_time.hour + self.start_time.minute / 60
            end_date = self.star_date + timedelta(hours=self.total_time)
        if self.total_day > 0:
            end_date = self.star_date + timedelta(days=self.total_day)
        return end_date


class BoatDetails(BaseModel):
    # Relationships
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="details_boat")

    # Fields
    length = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    max_guest = models.IntegerField(default=0)
    cabin = models.IntegerField(default=0)

    def __str__(self):
        return str(self.boat.boat_name)

    def get_absolute_url(self):
        return reverse("boat_BoatDetails_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatDetails_update", args=(self.pk,))


class BoatFAQ(BaseModel):
    # Relationships
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="faq_boat")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return str(self.boat.boat_name)

    def get_absolute_url(self):
        return reverse("boat_BoatFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatFAQ_update", args=(self.pk,))


class BoatPricing(BaseModel):
    # Relationships
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="pricing_boat")
    ticket_type = models.ForeignKey("boat.BoatTicketType", on_delete=models.CASCADE, related_name="ticket_pricing_boat")

    # Fields
    fixed_price = models.JSONField(default=dict, blank=True, null=True)
    extra_price = models.JSONField(default=dict, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        # return str(self.price)
        return f"{self.boat.boat_name} {self.price}"

    def get_absolute_url(self):
        return reverse("boat_BoatPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatPricing_update", args=(self.pk,))


class BoatReview(BaseModel):
    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_boat")
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="review_boat")

    # Fields
    rating = models.IntegerField(default=0)
    review_time = models.DateTimeField(auto_now_add=True)
    review = models.TextField()

    def __str__(self):
        return str(self.boat.boat_name)

    def get_absolute_url(self):
        return reverse("boat_BoatReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatReview_update", args=(self.pk,))


class BoatSpecs(BaseModel):
    # Relationships
    boat = models.ForeignKey("boat.Boat", on_delete=models.CASCADE, related_name="specs_boat")

    # Fields
    engines = models.CharField(max_length=255)
    year = models.DateField()
    fuel = models.CharField(max_length=255)
    total_crew = models.IntegerField(default=0)
    boat_model = models.CharField(max_length=255)
    boat_skipper = models.CharField(max_length=255)
    boat_manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return str(self.boat.boat_name)

    def get_absolute_url(self):
        return reverse("boat_BoatSpecs_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatSpecs_update", args=(self.pk,))


class BoatTicketType(BaseModel):
    # Fields
    is_active = models.BooleanField(default=True)
    total_ticket = models.IntegerField(default=0)
    ticket_type = models.IntegerField(default=0)

    def __str__(self):
        return str(f"{self.ticket_type} - {self.total_ticket}")

    def get_absolute_url(self):
        return reverse("boat_BoatTicketType_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("boat_BoatTicketType_update", args=(self.pk,))


@receiver(post_save, sender=BoatReview)
def update_average_rating(sender, instance, **kwargs):
    boat = instance.boat

    # Calculate the new average rating
    all_reviews = BoatReview.objects.filter(boat=boat)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        boat.average_rating = round(average_rating)
    else:
        boat.average_rating = 0

    boat.save()