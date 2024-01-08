from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from vendor import vendor_permissions
from . import vendorserializers
from ..website import serializers
from space import models

from django_filters import rest_framework as dj_filters
from space import filters


class AdminSpaceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Space class"""

    queryset = models.Space.objects.all()
    serializer_class = serializers.SpaceSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceList


# class SpaceBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceBooking class"""
#
#     queryset = models.SpaceBooking.objects.all()
#     serializer_class = serializers.SpaceBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminSpaceDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the SpaceDetails class"""

    queryset = models.SpaceDetails.objects.all()
    serializer_class = serializers.SpaceDetailsSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminSpaceFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the SpaceFAQ class"""

    queryset = models.SpaceFAQ.objects.all()
    serializer_class = serializers.SpaceFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminSpacePricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the SpacePricing class"""

    queryset = models.SpacePricing.objects.all()
    serializer_class = serializers.SpacePricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class SpaceReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceReview class"""
#
#     queryset = models.SpaceReview.objects.all()
#     serializer_class = serializers.SpaceReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminSpaceTicketTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the SpaceTicketType class"""

    queryset = models.SpaceTicketType.objects.all()
    serializer_class = serializers.SpaceTicketTypeSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminSpaceBookingViewSet(ListAPIView):
    queryset = models.SpaceBooking.objects.all()
    serializer_class = serializers.SpaceBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.SpaceBooking.objects.filter(space__owner=current_user.vendor_user.first())


class AdminSpaceBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.SpaceBooking.objects.all()
    serializer_class = vendorserializers.SpaceBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.space.owner == user_instance.vendor_user.first():
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
    #     if instance.space.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminSpaceReviewViewSet(ListAPIView):
    queryset = models.SpaceReview.objects.all()
    serializer_class = serializers.SpaceReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceReviewViewSet

