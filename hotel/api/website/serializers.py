from rest_framework import serializers

from hotel import models


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hotel
        fields = [
            "longitude",
            "hotel_star",
            "is_active",
            "hotel_type",
            "hotel_name",
            "discount",
            "highlights",
            "hotel_facilities",
            "average_rating",
            "description",
            "hotel_image",
            "hotel_services",
            "latitude",
            "owner",
            "location",
        ]
        read_only_fields = ("average_rating", "location", )


class HotelBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelBooking
        fields = [
            "booking_number",
            "quantity",
            "check_out",
            "check_in",
            "total_cost",
            "hotel",
            "customer",
            'room_type',
            "confirm_booking"
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', 'confirm_booking', )

    def validate(self, data):

        check_in = data.get('check_in')
        check_out = data.get('check_out')
        quantity = data.get('quantity')
        room_type = data.get('room_type')
        hotel = data.get('hotel')

        if check_in is None or check_out is None or quantity is None or hotel is None or hotel is room_type:
            raise serializers.ValidationError(" required.")

        if check_out < check_in:
            raise serializers.ValidationError("End date must be equal to or after the start date.")

        overlapping_bookings = models.HotelBooking.objects.filter(
            hotel=hotel,
            room_type=room_type,
            check_out__gte=check_in,
            check_in__lte=check_out
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This Hotel is already booked during the specified time.")

        return data


class HotelFAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelFAQ
        fields = [
            "faq",
            "hotel",
        ]


class HotelPricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelPricing
        fields = [
            "price",
            "room_type",
            "hotel",
            "fixed_price",
            "extra_price",
        ]


class HotelReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelReview
        fields = [
            "review_time",
            "review",
            "rating",
            "hotel",
            "customer",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        hotel = data.get('hotel')

        if hotel is None:
            raise serializers.ValidationError(" Rating and hotel is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class HotelRulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelRules
        fields = [
            "check_in",
            "check_out",
            "hotel_policies",
            "hotel",
        ]


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = [
            "room_type",
            "room_bed",
            "room_max_member",
            "room_max_member",
            "is_active",
            "room_size",
            "room_max_child",
            "hotel",
        ]
