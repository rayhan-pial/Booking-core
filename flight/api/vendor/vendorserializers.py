from rest_framework import serializers

from flight import models


class FlightBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FlightBooking
        fields = ["confirm_booking"]
