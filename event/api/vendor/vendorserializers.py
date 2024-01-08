from rest_framework import serializers

from event import models


class EventBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventBooking
        fields = ["confirm_booking"]


class EventDetailsAdminCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDetails
        fields = [
            "duration",
            "wishlist",
            "start_time",
            "event",
        ]
        read_only_fields = ('wishlist', )
