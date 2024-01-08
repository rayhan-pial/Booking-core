from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response

from vendor import vendor_permissions
from ..website import serializers
from car import models
from . import vendorserializers
from django_filters import rest_framework as dj_filters
from car import filters


class AdminCarViewSet(viewsets.ModelViewSet):
    """ViewSet for the Car class"""

    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCartList


# class CarBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarBooking class"""
#
#     queryset = models.CarBooking.objects.all()
#     serializer_class = serializers.CarBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission, ]

# vendor can get one serializer and have to post other serializer to accept booking

# def get_serializer_class(self):
#     if self.action in ["update", "partial_update"]:
#         return WritePostSerializer
#     return ReadPostSerializer

class AdminCarDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the CarDetails class"""

    queryset = models.CarDetails.objects.all()
    serializer_class = serializers.CarDetailsSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminCarFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the CarFAQ class"""

    queryset = models.CarFAQ.objects.all()
    serializer_class = serializers.CarFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminCarPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the CarPricing class"""

    queryset = models.CarPricing.objects.all()
    serializer_class = serializers.CarPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class CarReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarReview class"""
#
#     queryset = models.CarReview.objects.all()
#     serializer_class = serializers.CarReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminCarBookingViewSet(ListAPIView):
    queryset = models.CarBooking.objects.all()
    serializer_class = serializers.CarBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCarBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.CarBooking.objects.filter(car__owner=current_user.vendor_user.first())


class AdminCarBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.CarBooking.objects.all()
    serializer_class = vendorserializers.CarBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.car.owner == user_instance.vendor_user.first():
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
    #     print('----------------------------------')
    #     print(user_instance.vendor_user.first())
    #     print(instance.car.owner)
    #     if instance.car.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminCarReviewViewSet(ListAPIView):
    queryset = models.CarReview.objects.all()
    serializer_class = serializers.CarReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCarReviewViewSet
