from rest_framework import viewsets, permissions

from . import serializers
from customer import models


class customerViewSet(viewsets.ModelViewSet):
    """ViewSet for the customer class"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.customerSerializer
    permission_classes = [permissions.IsAuthenticated]
