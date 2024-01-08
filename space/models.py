import random
from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from coreapp.base import BaseModel
from helper import location


class Space(BaseModel):
    # Relationships
    owner = models.ForeignKey("vendor.vendor", on_delete=models.CASCADE, related_name="vendor_space")

    # Fields
    space_name = models.CharField(max_length=255)
    amenities = models.JSONField(default=dict, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    is_active = models.BooleanField(default=True)
    average_rating = models.PositiveIntegerField(default=0)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.00)
    space_image = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="space_image",
                                    null=True, blank=True)
    space_type = models.JSONField(default=dict, blank=True, null=True)
    highlights = models.JSONField(default=dict, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=255)


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_Space_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_Space_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.location = location.get_location_name(self.latitude, self.longitude)

        super(Space, self).save(*args, **kwargs)


class SpaceBooking(BaseModel):
    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_booking_space")
    space = models.ForeignKey("space.Space", on_delete=models.CASCADE, related_name="booking_space")

    # Fields
    booking_number = models.IntegerField(default=0)
    star_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    end_date = models.DateTimeField()
    ticket_type = ArrayField(models.IntegerField(default=0))
    ticket_quantity = ArrayField(models.IntegerField(default=0))
    confirm_booking = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpaceBooking_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpaceBooking_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost
        self.booking_number = self.generate_booking_number()

        super(SpaceBooking, self).save(*args, **kwargs)

    @staticmethod
    def generate_booking_number():
        # Generate a random 6-digit booking number
        return random.randint(100000, 999999)

    @property
    def calculate_total_cost(self):
        """
        Calculate the total cost based on the pricing details of the associated .
        """
        # if (not self.space or not self.star_date or not self.end_date or not self.ticket_type or not
        #         self.ticket_quantity):
        #     return 0.00

        # Calculate the duration of the booking in days
        duration_days = (self.end_date - self.star_date).days + 1

        # adult_space_pricing = self.space.pricing_space.get(ticket_type=self.adult_ticket_type)
        #
        # if self.child_ticket_type >0 and self.child_quantity >0:
        #     child_space_pricing = self.space.pricing_space.get(ticket_type=self.child_ticket_type)
        #
        #     # Get the pricing details of the associated car
        # # space_pricing = self.space.pricing_space.first()
        #
        # if not adult_space_pricing:
        #     return 0.00
        # # if not adult_space_pricing:
        # #     return 0.00
        #
        # # Calculate the total cost
        # adult_base_price = adult_space_pricing.price * duration_days * self.quantity
        # child_base_price = child_space_pricing.price * duration_days * self.quantity
        # fixed_price = sum(adult_space_pricing.fixed_price.values())
        # extra_price = sum(adult_space_pricing.extra_price.values()) if adult_space_pricing.extra_price else 0.00
        #
        # total_cost = adult_base_price + fixed_price + extra_price + child_base_price
        #
        # return total_cost
        total_cost = 0
        for ticket, quantity in zip(self.ticket_type, self.ticket_quantity):
            # print(ticket)
            # print(type(quantity))
            space_pricing = SpacePricing.objects.filter(ticket_type=ticket)
            # print(space_pricing.first())
            # print('++++++++++++++++')
            space_price = space_pricing.first()

            # print(space_price)
            # print(space_price.first().price)
            base_price = space_price.price * duration_days * quantity
            # fixed_price = sum(space_price.fixed_price.values())
            fixed_price = sum(
                Decimal(value) for value in space_price.fixed_price.values())
            extra_price = sum(
                Decimal(value) for value in space_price.extra_price.values()) if space_price.extra_price else Decimal(
                '0.00')

            # extra_price = sum(space_price.extra_price.values()) if space_price.extra_price else 0.00
            total_cost += base_price + fixed_price + extra_price

        if self.space.discount > 0:
            discount_amount = (self.space.discount / 100) * total_cost
            total_cost = total_cost - discount_amount

        return total_cost


class SpaceDetails(BaseModel):
    # Relationships
    space = models.ForeignKey("space.Space", on_delete=models.CASCADE, related_name="details_space")

    # Fields
    is_active = models.BooleanField(default=True)
    total_bed = models.IntegerField(default=0)
    total_bathroom = models.IntegerField(default=0)
    max_people = models.IntegerField(default=0)
    size = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpaceDetails_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpaceDetails_update", args=(self.pk,))


class SpaceFAQ(BaseModel):
    # Relationships
    space = models.ForeignKey("space.Space", on_delete=models.CASCADE, related_name="faq_space")

    # Fields
    faq = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpaceFAQ_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpaceFAQ_update", args=(self.pk,))


class SpacePricing(BaseModel):
    # Relationships
    space = models.ForeignKey("space.Space", on_delete=models.CASCADE, related_name="pricing_space")
    ticket_type = models.ForeignKey("space.SpaceTicketType", on_delete=models.CASCADE,
                                    related_name="ticket_pricing_space")

    # Fields
    extra_price = models.JSONField(default=dict, blank=True, null=True)
    fixed_price = models.JSONField(default=dict, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpacePricing_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpacePricing_update", args=(self.pk,))


class SpaceReview(BaseModel):
    # Relationships
    customer = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="customer_review_space")
    space = models.ForeignKey("space.Space", on_delete=models.CASCADE, related_name="review_space")

    # Fields
    rating = models.IntegerField(default=0)
    review = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpaceReview_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpaceReview_update", args=(self.pk,))


class SpaceTicketType(BaseModel):
    # Fields
    is_active = models.BooleanField(default=True)
    ticket_type = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("space_SpaceTicketType_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("space_SpaceTicketType_update", args=(self.pk,))


@receiver(post_save, sender=SpaceReview)
def update_average_rating(sender, instance, **kwargs):
    space = instance.space

    # Calculate the new average rating
    all_reviews = SpaceReview.objects.filter(space=space)
    total_reviews = all_reviews.count()

    if total_reviews > 0:
        average_rating = sum(review.rating for review in all_reviews) / total_reviews
        space.average_rating = round(average_rating)
    else:
        space.average_rating = 0

    space.save()
