import random

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Flight(BaseModel):

    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_flight")

    # Fields
    flight_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="flight_image",
                                     null=True, blank=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    departure_time = models.DateTimeField()
    arrival_location = models.CharField(max_length=255)
    departure_location = models.CharField(max_length=255)
    flight_name = models.CharField(max_length=255)
    arrival_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    inflight_experience = models.JSONField(default=dict, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating = models.PositiveIntegerField(default=0)

    class Meta:
        pass

    def __str__(self):
        return str(self.flight_name)

    def get_absolute_url(self):
        return reverse("flight_Flight_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_Flight_update", args=(self.pk,))


class FlightBooking(BaseModel):

    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_flight")
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE, related_name="booking_flight")

    # Fields
    booking_number = models.IntegerField()
    # quantity = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_type = ArrayField(models.IntegerField(default=0))
    ticket_quantity = ArrayField(models.IntegerField(default=0))
    confirm_booking = models.BooleanField(default=False)

    def __str__(self):
        return str(self.flight.flight_name)

    def get_absolute_url(self):
        return reverse("flight_FlightBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_FlightBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()

        super(FlightBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        # if not self.flight or not self.quantity:
        #     return 0.00

        # Calculate the duration of the booking in days

        # Get the pricing details of the associated car
        # flight_pricing = self.flight.pricing_flight.first()
        #
        # if not flight_pricing:
        #     return 0.00
        #
        # # Calculate the total cost
        # base_price = flight_pricing.price * self.quantity
        # fixed_price = sum(flight_pricing.fixed_price.values())
        # extra_price = sum(flight_pricing.extra_price.values()) if flight_pricing.extra_price else 0.00
        #
        # total_cost = base_price + fixed_price + extra_price
        # return total_cost
        # print('-------------------------------------')
        # print((self.ticket_type))
        total_cost = 0
        for ticket, quantity in zip(self.ticket_type, self.ticket_quantity):
            # print(ticket)
            # print(type(quantity))
            flight_pricing = FlightPricing.objects.filter(flight_type=ticket)
            # print('++++++++++++++++')
            flight_price = flight_pricing.first()
            # print('++++++++++++++++')
            # print(flight_pricing.first())
            # print(flight_pricing.first().price)
            base_price = flight_price.price * quantity
            total_cost += base_price

        if self.flight.discount > 0:
            discount_amount = (self.flight.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class FlightFAQ(BaseModel):

    # Relationships
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE, related_name="faq_flight")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("flight_FlightFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_FlightFAQ_update", args=(self.pk,))


class FlightPricing(BaseModel):

    # Relationships
    flight_type = models.ForeignKey("flight.FlightSeatType", on_delete=models.CASCADE,
                                    related_name="ticket_pricing_flight")
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE, related_name="pricing_flight")

    # Fields
    cabin = models.IntegerField()
    baggage = models.IntegerField()
    check_in = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("flight_FlightPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_FlightPricing_update", args=(self.pk,))


class FlightReview(BaseModel):

    # Relationships
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE, related_name="review_flight")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_flight")

    # Fields
    review = models.TextField()
    rating = models.IntegerField(default=0)
    review_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("flight_FlightReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_FlightReview_update", args=(self.pk,))


class FlightSeatType(BaseModel):

    # Fields
    is_active = models.BooleanField(default=True)
    passenger_type = models.IntegerField()
    seat_type = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("flight_FlightSeatType_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("flight_FlightSeatType_update", args=(self.pk,))
