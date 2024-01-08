from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from vendor import vendor_permissions
from . import vendorserializers
from ..website import serializers
from flight import models

from django_filters import rest_framework as dj_filters
from flight import filters


class AdminFlightViewSet(viewsets.ModelViewSet):
    """ViewSet for the Flight class"""

    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightList


# class FlightBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightBooking class"""
#
#     queryset = models.FlightBooking.objects.all()
#     serializer_class = serializers.FlightBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminFlightFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the FlightFAQ class"""

    queryset = models.FlightFAQ.objects.all()
    serializer_class = serializers.FlightFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminFlightPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the FlightPricing class"""

    queryset = models.FlightPricing.objects.all()
    serializer_class = serializers.FlightPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class FlightReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightReview class"""
#
#     queryset = models.FlightReview.objects.all()
#     serializer_class = serializers.FlightReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminFlightSeatTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the FlightSeatType class"""

    queryset = models.FlightSeatType.objects.all()
    serializer_class = serializers.FlightSeatTypeSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminFlightBookingViewSet(ListAPIView):
    queryset = models.FlightBooking.objects.all()
    serializer_class = serializers.FlightBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.FlightBooking.objects.filter(flight__owner=current_user.vendor_user.first())


class AdminFlightBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.FlightBooking.objects.all()
    serializer_class = vendorserializers.FlightBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.flight.owner == user_instance.vendor_user.first():
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to update this booking."},
                status=status.HTTP_403_FORBIDDEN
            )

    # def perform_update(self, serializer):
    #     instance = serializer.instance
    #     user_instance = self.request.user
    #     if instance.flight.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminFlightReviewViewSet(ListAPIView):
    queryset = models.FlightReview.objects.all()
    serializer_class = serializers.FlightReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightReviewViewSet
