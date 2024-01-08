from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from . import vendorserializers
from ..website import serializers
from boat import models
from customer import customer_permissions
from vendor import vendor_permissions
from django_filters import rest_framework as dj_filters
from boat import filters


class BoatAdminViewSet(viewsets.ModelViewSet):
    """ViewSet for the Boat class"""

    queryset = models.Boat.objects.all()
    serializer_class = serializers.BoatSerializer
    permission_classes = [vendor_permissions.VendorPermission, ]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatList


# class BoatBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatBooking class"""
#
#     queryset = models.BoatBooking.objects.all()
#     serializer_class = serializers.BoatBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission, ]

# vendor can get one serializer and have to post other serializer to accept booking

# def get_serializer_class(self):
#     if self.action in ["update", "partial_update"]:
#         return WritePostSerializer
#     return ReadPostSerializer


class AdminBoatDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the BoatDetails class"""

    queryset = models.BoatDetails.objects.all()
    serializer_class = serializers.BoatDetailsSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminBoatFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the BoatFAQ class"""

    queryset = models.BoatFAQ.objects.all()
    serializer_class = serializers.BoatFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminBoatPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the BoatPricing class"""

    queryset = models.BoatPricing.objects.all()
    serializer_class = serializers.BoatPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class BoatReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatReview class"""
#
#     queryset = models.BoatReview.objects.all()
#     serializer_class = serializers.BoatReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminBoatSpecsViewSet(viewsets.ModelViewSet):
    """ViewSet for the BoatSpecs class"""

    queryset = models.BoatSpecs.objects.all()
    serializer_class = serializers.BoatSpecsSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminBoatTicketTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the BoatTicketType class"""

    queryset = models.BoatTicketType.objects.all()
    serializer_class = serializers.BoatTicketTypeSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminBoatBookingViewSet(ListAPIView):
    queryset = models.BoatBooking.objects.all()
    serializer_class = serializers.BoatBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.BoatBooking.objects.filter(boat__owner=current_user.vendor_user.first())


class AdminBoatBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.BoatBooking.objects.all()
    serializer_class = vendorserializers.BoatBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.boat.owner == user_instance.vendor_user.first():
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
    #     print(instance.boat.owner)
    #     if instance.boat.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminBoatReviewViewSet(ListAPIView):
    queryset = models.BoatReview.objects.all()
    serializer_class = serializers.BoatReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatReviewViewSet
