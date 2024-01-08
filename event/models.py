import random
from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Event(BaseModel):

    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_event")

    # Fields
    event_type = models.JSONField(default=dict, blank=True, null=True)
    average_rating = models.PositiveIntegerField(default=0)
    event_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="event_image",
                                    null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    highlight = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    event_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    location = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.event_name)

    def get_absolute_url(self):
        return reverse("event_Event_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_Event_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Event, self).save(*args, **kwargs)


class EventBooking(BaseModel):

    # Relationships
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="booking_event")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_event")
    # ticket_type = models.ForeignKey("event.EventTicketType", on_delete=models.CASCADE,
    #                                 related_name="ticket_booking_event")

    # Fields
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    star_date = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    booking_number = models.IntegerField()
    ticket_type = ArrayField(models.IntegerField(default=0))
    ticket_quantity = ArrayField(models.IntegerField(default=0))
    confirm_booking = models.BooleanField(default=False)

    def __str__(self):
        return str(self.event.event_name)

    def get_absolute_url(self):
        return reverse("event_EventBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()
        super(EventBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        if not self.event or not self.star_date:
            return 0.00

        # Calculate the duration of the booking in days
        # duration_days = (self.end_date - self.star_date).days + 1

        # Get the pricing details of the associated car
        # event_pricing = self.event.pricing_event.first()
        # print('++++++++++++++++++++++++++++++++')
        # event_pricing = self.event.pricing_event.first()
        # # print('=============+++++++++++++++==================')
        # # print(event_pricing)
        # if not event_pricing:
        #     return 0.00
        total_cost = 0
        for ticket, quantity in zip(self.ticket_type,self.ticket_quantity):
            # print(ticket)
            # print(type(quantity))
            event_pricing = EventPricing.objects.filter(ticket_type=int(ticket))
            event_price=event_pricing.first()
            # print('++++++++++++++++')
            # print(event_pricing.first())
            # print(event_pricing.first().price)
            base_price = event_price.price * quantity
            # fixed_price = sum(event_price.fixed_price.values())
            # extra_price = sum(event_price.extra_price.values()) if event_price.extra_price else 0.00

            fixed_price = sum(
                Decimal(value) for value in event_price.fixed_price.values())
            extra_price = sum(
                Decimal(value) for value in event_price.extra_price.values()) if event_price.extra_price else Decimal(
                '0.00')
            total_cost += base_price + fixed_price + extra_price

        if self.event.discount > 0:
            discount_amount = (self.event.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class EventDetails(BaseModel):

    # Relationships
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="details_event")

    # Fields
    duration = models.PositiveIntegerField(default=0)
    wishlist = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()

    class Meta:
        pass

    def __str__(self):
        return str(self.event.event_name)

    def get_absolute_url(self):
        return reverse("event_EventDetails_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventDetails_update", args=(self.pk,))


class EventFAQ(BaseModel):

    # Relationships
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="faq_event")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.event.event_name)

    def get_absolute_url(self):
        return reverse("event_EventFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventFAQ_update", args=(self.pk,))


class EventPricing(BaseModel):

    # Relationships
    ticket_type = models.ForeignKey("event.EventTicketType", on_delete=models.CASCADE,
                                    related_name="ticket_pricing_event")
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="pricing_event")

    # Fields
    fixed_price = models.JSONField(default=dict, blank=True, null=True)
    extra_price = models.JSONField(default=dict)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.event.event_name)

    def get_absolute_url(self):
        return reverse("event_EventPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventPricing_update", args=(self.pk,))


class EventReview(BaseModel):

    # Relationships
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="review_event")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_event")

    # Fields
    rating = models.PositiveIntegerField(default=0)
    review = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.event.event_name)

    def get_absolute_url(self):
        return reverse("event_EventReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventReview_update", args=(self.pk,))


class EventTicketType(BaseModel):

    # Fields
    is_active = models.BooleanField(default=True)
    ticket_type = models.PositiveIntegerField(default=0)
    total_ticket = models.PositiveIntegerField(default=0)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("event_EventTicketType_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("event_EventTicketType_update", args=(self.pk,))


@receiver(post_save, sender=EventReview)
def update_average_rating(sender, instance, **kwargs):
    event = instance.event

    # Calculate the new average rating
    all_reviews = EventReview.objects.filter(event=event)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        event.average_rating = round(average_rating)
    else:
        event.average_rating = 0

    event.save()


class UserWishList(BaseModel):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="wishlist_event")
    wish = models.BooleanField(default=False)
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_wishlist")


    def __str__(self):
        return str(self.event.event_name)


@receiver(post_save, sender=UserWishList)
def update_total_wishlist(sender, instance, **kwargs):
    event = instance.event

    # Calculate count for wished event
    total_wishes=UserWishList.objects.filter(event=event, wish=True).count()

    event_details = EventDetails.objects.get(event=event)
    event_details.wishlist = total_wishes
    event_details.save()
