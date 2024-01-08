from rest_framework import serializers

from flight import models


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Flight
        fields = [
            "flight_image",
            "description",
            "discount",
            "departure_time",
            "arrival_location",
            "departure_location",
            "flight_name",
            "arrival_time",
            "is_active",
            "inflight_experience",
            "duration",
            "average_rating",
            "owner",
        ]
        read_only_fields =('average_rating', )


class FlightBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightBooking
        fields = [
            "booking_number",
            # "quantity",
            "total_cost",
            "ticket_type",
            "ticket_quantity",
            "customer",
            "flight",
            'confirm_booking',
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', 'confirm_booking', )

    # def validate(self, data):
    #
    #     quantity = data.get('quantity')
    #     flight = data.get('flight')
    #
    #     if quantity is None or flight is None:
    #         raise serializers.ValidationError("Are required.")
    #
    #     return data


class FlightFAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightFAQ
        fields = [
            "faq",
            "flight",
        ]


class FlightPricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightPricing
        fields = [
            "cabin",
            "baggage",
            "check_in",
            "price",
            "flight_type",
            "flight",
        ]


class FlightReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightReview
        fields = [
            "review",
            "rating",
            "review_time",
            "flight",
            "customer",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        flight = data.get('flight')

        if flight is None:
            raise serializers.ValidationError("flight is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class FlightSeatTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightSeatType
        fields = [
            "is_active",
            "passenger_type",
            "seat_type",
        ]
