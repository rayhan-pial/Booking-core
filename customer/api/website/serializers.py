from rest_framework import serializers

from customer import models


class customerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = [
            "location",
        ]
