from rest_framework import serializers

from car import models


class CarBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CarBooking
        fields = ["confirm_booking"]
