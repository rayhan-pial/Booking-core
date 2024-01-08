from rest_framework import serializers

from space import models


class SpaceBookingAdminUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceBooking
        fields = ["confirm_booking"]
