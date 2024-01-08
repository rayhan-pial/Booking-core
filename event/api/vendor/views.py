from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from vendor import vendor_permissions
from . import vendorserializers
from ..website import serializers
from event import models
from django_filters import rest_framework as dj_filters
from event import filters


class AdminEventViewSet(viewsets.ModelViewSet):
    """ViewSet for the Event class"""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterEventList


# class EventBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventBooking class"""
#
#     queryset = models.EventBooking.objects.all()
#     serializer_class = serializers.EventBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminEventDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the EventDetails class"""

    queryset = models.EventDetails.objects.all()
    # serializer_class = serializers.EventDetailsSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return vendorserializers.EventDetailsAdminCUDSerializer
        else:
            return serializers.EventDetailsSerializer


class AdminEventFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the EventFAQ class"""

    queryset = models.EventFAQ.objects.all()
    serializer_class = serializers.EventFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminEventPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the EventPricing class"""

    queryset = models.EventPricing.objects.all()
    serializer_class = serializers.EventPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class EventReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventReview class"""
#
#     queryset = models.EventReview.objects.all()
#     serializer_class = serializers.EventReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminEventTicketTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the EventTicketType class"""

    queryset = models.EventTicketType.objects.all()
    serializer_class = serializers.EventTicketTypeSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminEventBookingViewSet(ListAPIView):
    queryset = models.EventBooking.objects.all()
    serializer_class = serializers.EventBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.EventBooking.objects.filter(event__owner=current_user.vendor_user.first())


class AdminEventBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.EventBooking.objects.all()
    serializer_class = vendorserializers.EventBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_instance = self.request.user

        if instance.event.owner == user_instance.vendor_user.first():
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
    #     if instance.event.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )


class AdminEventReviewViewSet(ListAPIView):
    queryset = models.EventReview.objects.all()
    serializer_class = serializers.EventReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterEventReviewViewSet
