from rest_framework import serializers

from vendor import models


class vendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.vendor
        fields = [
            'location',
            'user',
        ]
