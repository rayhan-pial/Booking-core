from rest_framework import serializers

from tour import models


class TourBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TourBooking
        fields = ["confirm_booking"]
