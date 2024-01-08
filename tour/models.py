import random
from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Tour(BaseModel):

    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_tour")

    # Fields
    is_active = models.BooleanField(default=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    average_rating = models.PositiveIntegerField(default=0)
    highlights = models.JSONField(default=dict, blank=True, null=True)
    tour_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="tour_image",
                                   null=True, blank=True)
    exclude = models.JSONField(default=dict, blank=True, null=True)
    facilities = models.JSONField(default=dict, blank=True, null=True)
    overview = models.TextField()
    tour_type = models.JSONField(default=dict, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    tour_name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    travel_style = models.JSONField(default=dict, blank=True, null=True)
    include = models.JSONField(default=dict, blank=True, null=True)
    location = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_Tour_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_Tour_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Tour, self).save(*args, **kwargs)


class TourBooking(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="booking_tour")
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_tour")

    # Fields
    booking_number = models.IntegerField(default=0)
    star_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_type = ArrayField(models.IntegerField(default=0))
    ticket_quantity = ArrayField(models.IntegerField(default=0))
    confirm_booking = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.tour.tour_name)

    # def get_absolute_url(self):
    #     return reverse("tour_TourBooking_detail", args=(self.pk,))
    #
    # def get_update_url(self):
    #     return reverse("tour_TourBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        self.booking_number = self.generate_booking_number()

        super(TourBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated car.
        """
        if not self.tour or not self.star_date or not self.ticket_type or not self.ticket_quantity:
            return 0.00

        # tour_pricing = self.tour.pricing_tour.first()
        #
        # if not tour_pricing:
        #     return 0.00
        #
        # # Calculate the total cost
        # base1_price = tour_pricing.price * self.total_adult
        # base2_price = tour_pricing.price * self.total_child
        #
        # fixed_price = sum(tour_pricing.fixed_price.values())
        # extra_price = sum(tour_pricing.extra_price.values()) if tour_pricing.extra_price else 0.00
        #
        # total_cost = base1_price + base2_price + fixed_price + extra_price
        # return total_cost
        total_cost = 0
        for ticket, quantity in zip(self.ticket_type, self.ticket_quantity):
            # print(ticket)
            # print(type(quantity))
            event_pricing = TourPricing.objects.filter(ticket_type=ticket)
            event_price = event_pricing.first()
            # print('++++++++++++++++')
            # print(event_pricing.first())
            # print(event_pricing.first().price)
            base_price = event_price.price * quantity
            # fixed_price = sum(event_price.fixed_price.values())
            fixed_price = sum(Decimal(value) for value in event_price.fixed_price.values())
            extra_price = sum(
                Decimal(value) for value in event_price.extra_price.values()) if event_price.extra_price else 0.00

            # extra_price = sum(event_price.extra_price.values()) if event_price.extra_price else 0.00
            total_cost += base_price + fixed_price + extra_price

        if self.tour.discount > 0:
            discount_amount = (self.tour.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class TourDetails(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="details_tour")

    # Fields
    group_size = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    duration = models.IntegerField(default=0)
    location = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourDetails_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourDetails_update", args=(self.pk,))


class TourFAQ(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="faq_tour")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourFAQ_update", args=(self.pk,))


class TourItinerary(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="itinerary_tour")

    # Fields
    itinerary_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE,
                                        related_name="tour_itinerary_image", null=True, blank=True)
    day = models.CharField(max_length=30)
    details = models.TextField()
    title = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourItinerary_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourItinerary_update", args=(self.pk,))


class TourPricing(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="pricing_tour")
    ticket_type = models.ForeignKey("tour.TourTicketType", on_delete=models.CASCADE, related_name="ticket_pricing_tour")

    # Fields
    extra_price = models.JSONField(default=dict, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fixed_price = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourPricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourPricing_update", args=(self.pk,))


class TourReview(BaseModel):

    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_tour")
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="review_tour")

    # Fields
    review = models.TextField()
    rating = models.IntegerField(default=0)
    review_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourReview_update", args=(self.pk,))


class TourRules(BaseModel):

    # Relationships
    tour = models.ForeignKey("tour.Tour", on_delete=models.CASCADE, related_name="rules_tour")

    # Fields
    rule = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourRules_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourRules_update", args=(self.pk,))


class TourTicketType(BaseModel):

    # Fields
    ticket_type = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("tour_TourTicketType_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("tour_TourTicketType_update", args=(self.pk,))


@receiver(post_save, sender=TourReview)
def update_average_rating(sender, instance, **kwargs):
    tour = instance.tour

    # Calculate the new average rating
    all_reviews = TourReview.objects.filter(tour=tour)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        tour.average_rating = round(average_rating)
    else:
        tour.average_rating = 0

    tour.save()