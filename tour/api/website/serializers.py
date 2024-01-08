from rest_framework import serializers

from tour import models


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tour
        fields = [
            "is_active",
            "longitude",
            "average_rating",
            "highlights",
            "tour_image",
            "exclude",
            "facilities",
            "overview",
            "tour_type",
            "latitude",
            "tour_name",
            "discount",
            "travel_style",
            "include",
            "owner",
            "location",
        ]
        read_only_fields = ("average_rating", "location", )


class TourBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourBooking
        fields = [
            "booking_number",
            "star_date",
            "total_cost",
            "tour",
            "ticket_type",
            "ticket_quantity",
            "customer",
            "confirm_booking",
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', 'confirm_booking', )

    def validate(self, data):
        start_date = data.get('star_date')

        if start_date is None:
            raise serializers.ValidationError("Start date required.")

        return data


class TourDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourDetails
        fields = [
            "group_size",
            "is_active",
            "duration",
            "location",
            "tour",
        ]


class TourFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourFAQ
        fields = [
            "faq",
            "tour",
        ]


class TourItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourItinerary
        fields = [
            "itinerary_image",
            "day",
            "details",
            "title",
            "tour",
        ]


class TourPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourPricing
        fields = [
            "extra_price",
            "price",
            "fixed_price",
            "tour",
            "ticket_type",
        ]


class TourReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourReview
        fields = [
            "review",
            "rating",
            "review_time",
            "customer",
            "tour",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        tour = data.get('tour')

        if tour is None:
            raise serializers.ValidationError(" Rating and tour is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class TourRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourRules
        fields = [
            "rule",
            "tour",
        ]


class TourTicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TourTicketType
        fields = [
            "ticket_type",
            "is_active",
        ]
