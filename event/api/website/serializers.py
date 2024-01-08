from rest_framework import serializers

from event import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            "event_type",
            "average_rating",
            "event_image",
            "longitude",
            "highlight",
            "is_active",
            "description",
            "discount",
            "event_name",
            "latitude",
            "owner",
            "location",
        ]

        read_only_fields = ("average_rating", "location", )


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventBooking
        fields = [
            "total_cost",
            "star_date",
            # "quantity",
            "booking_number",
            "event",
            "customer",
            "ticket_type",
            "ticket_quantity",
            'confirm_booking',
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', 'confirm_booking', )

    def validate(self, data):

        start_date = data.get('star_date')
        event = data.get('event')
        ticket_type = data.get('ticket_type')

        if start_date is None or event is None or ticket_type is None:
            raise serializers.ValidationError(" required.")

        return data

    # def create(self, validated_data):
    #     ticket_type = validated_data.pop('ticket_type')
    #     ticket_quantity = validated_data.pop('ticket_quantity')
    #
    #     for ticket,quantity in zip(ticket_type,ticket_quantity):
    #
    #         event_pricing=models.EventPricing.objects.filter(ticket_type=ticket)
    #         base_price = event_pricing.price * quantity
    #         fixed_price = sum(event_pricing.fixed_price.values())
    #         extra_price = sum(event_pricing.extra_price.values()) if event_pricing.extra_price else 0.00
    #         total_cost = base_price + fixed_price + extra_price




class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDetails
        fields = [
            "duration",
            "wishlist",
            "start_time",
            "event",
        ]


class WishlistEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDetails
        fields = [
            "wishlist",
            "event",
        ]


class EventFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventFAQ
        fields = [
            "faq",
            "event",
        ]


class EventPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventPricing
        fields = [
            "fixed_price",
            "extra_price",
            "price",
            "ticket_type",
            "event",
        ]


class EventReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventReview
        fields = [
            "rating",
            "review",
            "review_time",
            "event",
            "customer",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        event = data.get('event')

        if event is None:
            raise serializers.ValidationError(" Rating and event is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class EventTicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventTicketType
        fields = [
            "is_active",
            "ticket_type",
        ]


class UserWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWishList
        fields = [
            "event",
            "wish",
            "customer",
        ]
        read_only_fields = ('customer', )
