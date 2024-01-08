from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from . import serializers
from hotel import models

from django_filters import rest_framework as dj_filters
from hotel import filters


# class HotelViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Hotel class"""
#
#     queryset = models.Hotel.objects.all()
#     serializer_class = serializers.HotelSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class HotelBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelBooking class"""
#
#     queryset = models.HotelBooking.objects.all()
#     serializer_class = serializers.HotelBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class HotelFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelFAQ class"""
#
#     queryset = models.HotelFAQ.objects.all()
#     serializer_class = serializers.HotelFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class HotelPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelPricing class"""
#
#     queryset = models.HotelPricing.objects.all()
#     serializer_class = serializers.HotelPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class HotelReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelReview class"""
#
#     queryset = models.HotelReview.objects.all()
#     serializer_class = serializers.HotelReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class HotelRulesViewSet(viewsets.ModelViewSet):
#     """ViewSet for the HotelRules class"""
#
#     queryset = models.HotelRules.objects.all()
#     serializer_class = serializers.HotelRulesSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class RoomViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Room class"""
#
#     queryset = models.Room.objects.all()
#     serializer_class = serializers.RoomSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerHotelViewSet(ListAPIView):
    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelList


class CustomerHotelBookingViewSet(ListCreateAPIView):
    queryset = models.HotelBooking.objects.all()
    serializer_class = serializers.HotelBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerHotelFAQViewSet(ListAPIView):
    queryset = models.HotelFAQ.objects.all()
    serializer_class = serializers.HotelFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerHotelPricingViewSet(ListAPIView):
    queryset = models.HotelPricing.objects.all()
    serializer_class = serializers.HotelPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerHotelReviewViewSet(viewsets.ModelViewSet):
    queryset = models.HotelReview.objects.all()
    serializer_class = serializers.HotelReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterHotelReviewViewSet

    def create(self, request, *args, **kwargs):
        hotel_id = request.data.get('hotel')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_hotel = models.HotelBooking.objects.filter(
            hotel=hotel_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_hotel:
            return Response({"message": "Have to book first to review"}, status=status.HTTP_400_BAD_REQUEST)

        reviewed_hotel = models.HotelReview.objects.filter(
            hotel=hotel_id,
            customer=customer_instance).exists()

        if reviewed_hotel:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        hotel_id = request.data.get('hotel')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_hotel = models.HotelReview.objects.filter(
            hotel=hotel_id,
            customer=customer_instance).exists()

        if not reviewed_hotel:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_hotel = models.HotelBooking.objects.filter(
            hotel=hotel_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_hotel:
            return Response({"message": "You did not book the hotel."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     hotel_id = serializer.validated_data.get('hotel')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_hotel = models.HotelBooking.objects.filter(
    #         hotel=hotel_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #
    #     if not booked_hotel:
    #         return Response({"message": "Have to book first to review"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_hotel = models.HotelReview.objects.filter(
    #         hotel=hotel_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_hotel:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerHotelRulesViewSet(ListAPIView):
    queryset = models.HotelRules.objects.all()
    serializer_class = serializers.HotelRulesSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerRoomViewSet(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [customer_permissions.CustomerPermission]
