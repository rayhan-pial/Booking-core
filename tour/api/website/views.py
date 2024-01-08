from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from . import serializers
from tour import models

from django_filters import rest_framework as dj_filters
from tour import filters


# class TourViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Tour class"""
#
#     queryset = models.Tour.objects.all()
#     serializer_class = serializers.TourSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourBooking class"""
#
#     queryset = models.TourBooking.objects.all()
#     serializer_class = serializers.TourBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourDetails class"""
#
#     queryset = models.TourDetails.objects.all()
#     serializer_class = serializers.TourDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourFAQ class"""
#
#     queryset = models.TourFAQ.objects.all()
#     serializer_class = serializers.TourFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourItineraryViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourItinerary class"""
#
#     queryset = models.TourItinerary.objects.all()
#     serializer_class = serializers.TourItinerarySerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourPricing class"""
#
#     queryset = models.TourPricing.objects.all()
#     serializer_class = serializers.TourPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourReview class"""
#
#     queryset = models.TourReview.objects.all()
#     serializer_class = serializers.TourReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourRulesViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourRules class"""
#
#     queryset = models.TourRules.objects.all()
#     serializer_class = serializers.TourRulesSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class TourTicketTypeViewSet(viewsets.ModelViewSet):
#     """ViewSet for the TourTicketType class"""
#
#     queryset = models.TourTicketType.objects.all()
#     serializer_class = serializers.TourTicketTypeSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourViewSet(ListAPIView):
    queryset = models.Tour.objects.all()
    serializer_class = serializers.TourSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourList


class CustomerTourBookingViewSet(ListCreateAPIView):
    queryset = models.TourBooking.objects.all()
    serializer_class = serializers.TourBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerTourDetailsViewSet(ListAPIView):
    queryset = models.TourDetails.objects.all()
    serializer_class = serializers.TourDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourFAQViewSet(ListAPIView):
    queryset = models.TourFAQ.objects.all()
    serializer_class = serializers.TourFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourItineraryViewSet(ListAPIView):
    queryset = models.TourItinerary.objects.all()
    serializer_class = serializers.TourItinerarySerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourPricingViewSet(ListAPIView):
    queryset = models.TourPricing.objects.all()
    serializer_class = serializers.TourPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourReviewViewSet(viewsets.ModelViewSet):
    queryset = models.TourReview.objects.all()
    serializer_class = serializers.TourReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterTourReviewViewSet

    def create(self, request, *args, **kwargs):
        tour_id = request.data.get('tour')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_tour = models.TourBooking.objects.filter(
            tour=tour_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_tour:
            return Response({"message": "Have to book first to review"},
                            status=status.HTTP_400_BAD_REQUEST)

        reviewed_tour = models.TourReview.objects.filter(
            tour=tour_id,
            customer=customer_instance).exists()

        if reviewed_tour:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        tour_id = request.data.get('tour')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_tour = models.TourReview.objects.filter(
            tour=tour_id,
            customer=customer_instance).exists()

        if not reviewed_tour:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_tour = models.TourBooking.objects.filter(
            tour=tour_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_tour:
            return Response({"message": "You did not book the tour."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     tour_id = serializer.validated_data.get('tour')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_tour = models.TourBooking.objects.filter(
    #         tour=tour_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #
    #     if not booked_tour:
    #         return Response({"message": "Have to book first to review"},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_tour = models.TourReview.objects.filter(
    #         tour=tour_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_tour:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerTourRulesViewSet(ListAPIView):
    queryset = models.TourRules.objects.all()
    serializer_class = serializers.TourRulesSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerTourTicketTypeViewSet(ListAPIView):
    queryset = models.TourTicketType.objects.all()
    serializer_class = serializers.TourTicketTypeSerializer
    permission_classes = [customer_permissions.CustomerPermission]