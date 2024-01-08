from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from vendor import vendor_permissions
from . import vendorserializers
from ..website import serializers
from hotel import models

from django_filters import rest_framework as dj_filters
from hotel import filters


class AdminHotelViewSet(viewsets.ModelViewSet):
    """ViewSet for the Hotel class"""

    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelList


# class HotelBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelBooking class"""
#
#     queryset = models.HotelBooking.objects.all()
#     serializer_class = serializers.HotelBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminHotelFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the HotelFAQ class"""

    queryset = models.HotelFAQ.objects.all()
    serializer_class = serializers.HotelFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminHotelPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the HotelPricing class"""

    queryset = models.HotelPricing.objects.all()
    serializer_class = serializers.HotelPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class HotelReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelReview class"""
#
#     queryset = models.HotelReview.objects.all()
#     serializer_class = serializers.HotelReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminHotelRulesViewSet(viewsets.ModelViewSet):
    """ViewSet for the HotelRules class"""

    queryset = models.HotelRules.objects.all()
    serializer_class = serializers.HotelRulesSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for the Room class"""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminHotelBookingViewSet(ListAPIView):
    queryset = models.HotelBooking.objects.all()
    serializer_class = serializers.HotelBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.HotelBooking.objects.filter(hotel__owner=current_user.vendor_user.first())


class AdminHotelBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.HotelBooking.objects.all()
    serializer_class = vendorserializers.HotelBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.hotel.owner == user_instance.vendor_user.first():
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
    #     if instance.hotel.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminHotelReviewViewSet(ListAPIView):
    queryset = models.HotelReview.objects.all()
    serializer_class = serializers.HotelReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelReviewViewSet

