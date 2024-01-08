from rest_framework import serializers

from boat import models


class BoatBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatBooking
        fields = ["confirm_booking"]
