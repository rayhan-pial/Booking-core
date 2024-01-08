from rest_framework import viewsets, permissions

from . import serializers
from vendor import models


class vendorViewSet(viewsets.ModelViewSet):
    """ViewSet for the vendor class"""

    queryset = models.vendor.objects.all()
    serializer_class = serializers.vendorSerializer
    permission_classes = [permissions.IsAuthenticated]
