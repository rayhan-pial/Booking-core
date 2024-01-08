from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from . import serializers
from flight import models

from django_filters import rest_framework as dj_filters
from flight import filters

# class FlightViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Flight class"""
#
#     queryset = models.Flight.objects.all()
#     serializer_class = serializers.FlightSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class FlightBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightBooking class"""
#
#     queryset = models.FlightBooking.objects.all()
#     serializer_class = serializers.FlightBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class FlightFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightFAQ class"""
#
#     queryset = models.FlightFAQ.objects.all()
#     serializer_class = serializers.FlightFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class FlightPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightPricing class"""
#
#     queryset = models.FlightPricing.objects.all()
#     serializer_class = serializers.FlightPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class FlightReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightReview class"""
#
#     queryset = models.FlightReview.objects.all()
#     serializer_class = serializers.FlightReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class FlightSeatTypeViewSet(viewsets.ModelViewSet):
#     """ViewSet for the FlightSeatType class"""
#
#     queryset = models.FlightSeatType.objects.all()
#     serializer_class = serializers.FlightSeatTypeSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerFlightViewSet(ListAPIView):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightList


class CustomerFlightBookingViewSet(ListCreateAPIView):
    queryset = models.FlightBooking.objects.all()
    serializer_class = serializers.FlightBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerFlightFAQViewSet(ListAPIView):
    queryset = models.FlightFAQ.objects.all()
    serializer_class = serializers.FlightFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerFlightPricingViewSet(ListAPIView):
    queryset = models.FlightPricing.objects.all()
    serializer_class = serializers.FlightPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerFlightReviewViewSet(viewsets.ModelViewSet):
    queryset = models.FlightReview.objects.all()
    serializer_class = serializers.FlightReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterFlightReviewViewSet

    def create(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_flight = models.FlightBooking.objects.filter(
            flight=flight_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_flight:
            return Response({"message": "Can't create a review. Please book the flight first."},
                            status=status.HTTP_400_BAD_REQUEST)

        reviewed_flight = models.FlightReview.objects.filter(
            flight=flight_id,
            customer=customer_instance).exists()

        if reviewed_flight:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_flight = models.FlightReview.objects.filter(
            flight=flight_id,
            customer=customer_instance).exists()

        if not reviewed_flight:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_flight = models.FlightBooking.objects.filter(
            flight=flight_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_flight:
            return Response({"message": "You did not book the flight."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     flight_id = serializer.validated_data.get('flight')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_flight = models.FlightBooking.objects.filter(
    #         flight=flight_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #     if not booked_flight:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_flight = models.FlightReview.objects.filter(
    #         flight=flight_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_flight:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerFlightSeatTypeViewSet(ListAPIView):
    queryset = models.FlightSeatType.objects.all()
    serializer_class = serializers.FlightSeatTypeSerializer
    permission_classes = [customer_permissions.CustomerPermission]
