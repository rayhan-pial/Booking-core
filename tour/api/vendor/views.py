from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from vendor import vendor_permissions
from . import vendorserializers
from ..website import serializers
from tour import models

from django_filters import rest_framework as dj_filters
from tour import filters


class AdminTourViewSet(viewsets.ModelViewSet):
    """ViewSet for the Tour class"""

    queryset = models.Tour.objects.all()
    serializer_class = serializers.TourSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourList


# class TourBookingAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourBooking class"""
#
#     queryset = models.TourBooking.objects.all()
#     serializer_class = serializers.TourBookingSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminTourDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourDetails class"""

    queryset = models.TourDetails.objects.all()
    serializer_class = serializers.TourDetailsSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminTourFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourFAQ class"""

    queryset = models.TourFAQ.objects.all()
    serializer_class = serializers.TourFAQSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminTourItineraryViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourItinerary class"""

    queryset = models.TourItinerary.objects.all()
    serializer_class = serializers.TourItinerarySerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminTourPricingViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourPricing class"""

    queryset = models.TourPricing.objects.all()
    serializer_class = serializers.TourPricingSerializer
    permission_classes = [vendor_permissions.VendorPermission]


# class TourReviewAdminViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourReview class"""
#
#     queryset = models.TourReview.objects.all()
#     serializer_class = serializers.TourReviewSerializer
#     permission_classes = [vendor_permissions.VendorPermission]


class AdminTourRulesViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourRules class"""

    queryset = models.TourRules.objects.all()
    serializer_class = serializers.TourRulesSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminTourTicketTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the TourTicketType class"""

    queryset = models.TourTicketType.objects.all()
    serializer_class = serializers.TourTicketTypeSerializer
    permission_classes = [vendor_permissions.VendorPermission]


class AdminTourBookingViewSet(ListAPIView):
    queryset = models.TourBooking.objects.all()
    serializer_class = serializers.TourBookingSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourBookingViewSet

    def get_queryset(self):
        current_user = self.request.user
        return models.TourBooking.objects.filter(tour__owner=current_user.vendor_user.first())


class AdminTourBookingUpdateViewsSet(UpdateAPIView):
    queryset = models.TourBooking.objects.all()
    serializer_class = vendorserializers.TourBookingAdminUpdateSerializer
    permission_classes = [vendor_permissions.VendorPermission]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_instance = self.request.user

        if instance.tour.owner == user_instance.vendor_user.first():
            serializer = self.get_serializer(instance, data=request.data, partial=self.partial_update)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to update this booking."},
                status=status.HTTP_403_FORBIDDEN)

    # def perform_update(self, serializer):
    #     instance = serializer.instance
    #     user_instance = self.request.user
    #
    #     if instance.tour.owner == user_instance.vendor_user.first():
    #         serializer.save()
    #     else:
    #         return Response(
    #             {"detail": "You do not have permission to update this booking."},
    #             status=status.HTTP_403_FORBIDDEN)


class AdminTourReviewViewSet(ListAPIView):
    queryset = models.TourReview.objects.all()
    serializer_class = serializers.TourReviewSerializer
    permission_classes = [vendor_permissions.VendorPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourReviewViewSet

