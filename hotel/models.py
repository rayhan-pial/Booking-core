import random
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Hotel(BaseModel):
    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_hotel")

    # Fields
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    hotel_star = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    hotel_type = models.JSONField(default=dict, blank=True, null=True)
    hotel_name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highlights = models.JSONField(default=dict, blank=True, null=True)
    hotel_facilities = models.JSONField(default=dict, blank=True, null=True)
    average_rating = models.PositiveIntegerField(default=0)
    description = models.TextField()
    hotel_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="hotel_image",
                                    null=True, blank=True)
    hotel_services = models.JSONField(default=dict, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    location = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_Hotel_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_Hotel_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Hotel, self).save(*args, **kwargs)


class HotelBooking(BaseModel):
    # Relationships
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="booking_hotel")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_hotel")

    # Fields
    booking_number = models.IntegerField()
    quantity = models.IntegerField(default=0)
    check_out = models.DateTimeField()
    check_in = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    room_type = models.IntegerField(default=0)
    confirm_booking = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_HotelBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_HotelBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()

        super(HotelBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        if not self.hotel or not self.check_in or not self.check_out or not self.quantity:
            return 0.00

        # Calculate the duration of the booking in days
        duration_days = (self.check_out - self.check_in).days + 1

        hotel_pricing = self.hotel.pricing_hotel.get(room_type=self.room_type)
        # print('+++++++++++++++++++++++++++++++')
        # print(hotel_pricing.price)

        # hotel_pricing = self.hotel.pricing_hotel.first()

        if not hotel_pricing:
            return 0.00

        # Calculate the total cost
        base_price = hotel_pricing.price * duration_days * self.quantity
        # fixed_price = sum(hotel_pricing.fixed_price.values())
        # extra_price = sum(hotel_pricing.extra_price.values()) if hotel_pricing.extra_price else 0.00

        fixed_price = sum(
            Decimal(value) for value in hotel_pricing.fixed_price.values())
        extra_price = sum(
            Decimal(value) for value in hotel_pricing.extra_price.values()) if hotel_pricing.extra_price else Decimal(
            '0.00')

        total_cost = base_price + fixed_price + extra_price

        if self.hotel.discount > 0:
            discount_amount = (self.hotel.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class HotelFAQ(BaseModel):
    # Relationships
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="faq_hotel")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_HotelFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_HotelFAQ_update", args=(self.pk,))


class HotelPricing(BaseModel):
    # Relationships
    room_type = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, related_name="room_pricing_hotel")
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="pricing_hotel")

    # Fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fixed_price = models.JSONField(default=dict, blank=True, null=True)
    extra_price = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_HotelPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_HotelPricing_update", args=(self.pk,))


class HotelReview(BaseModel):
    # Relationships
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="review_hotel")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_hotel")

    # Fields
    review_time = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    rating = models.IntegerField(default=0)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_HotelReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_HotelReview_update", args=(self.pk,))


class HotelRules(BaseModel):
    # Relationships
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="rules_hotel")

    # Fields
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    hotel_policies = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_HotelRules_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_HotelRules_update", args=(self.pk,))


class Room(BaseModel):
    # Relationships
    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE, related_name="room_hotel")

    # Fields
    room_type = models.IntegerField(default=0)
    room_bed = models.IntegerField(default=0)
    room_max_member = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    room_size = models.CharField(max_length=255)
    room_max_child = models.IntegerField(default=0)

    class Meta:
        pass

    def __str__(self):
        return str(self.hotel.hotel_name)

    def get_absolute_url(self):
        return reverse("hotel_Room_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("hotel_Room_update", args=(self.pk,))


@receiver(post_save, sender=HotelReview)
def update_average_rating(sender, instance, **kwargs):
    hotel = instance.hotel

    # Calculate the new average rating
    all_reviews = HotelReview.objects.filter(hotel=hotel)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        hotel.average_rating = round(average_rating)
    else:
        hotel.average_rating = 0

    hotel.save()
