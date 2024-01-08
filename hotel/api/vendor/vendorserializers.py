from rest_framework import serializers

from hotel import models


class HotelBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelBooking
        fields = ["confirm_booking"]
