from urllib import response

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.response import Response


from customer import customer_permissions, models
from customer.models import Customer
from . import serializers
from car import models
from django_filters import rest_framework as dj_filters
from car import filters
from django.utils.translation import gettext_lazy as _



# class UserCarViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Car class"""
#
#     queryset = models.Car.objects.all()
#     serializer_class = serializers.CarSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class UserCarBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarBooking class"""
#
#     queryset = models.CarBooking.objects.all()
#     serializer_class = serializers.CarBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]
#
#     def perform_create(self, serializer):
#         customer_instance = self.request.user.customer_user
#         serializer.save(customer=customer_instance)


# class CarBookingViewSet(viewsets.ModelViewSet):
#     queryset = models.CarBooking.objects.all()
#     serializer_class = serializers.CarBookingSerializer
#     permission_classes = [customer_permissions.CustomerCrudPermission]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)

# class UserCarDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarDetails class"""
#
#     queryset = models.CarDetails.objects.all()
#     serializer_class = serializers.CarDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class UserCarFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarFAQ class"""
#
#     queryset = models.CarFAQ.objects.all()
#     serializer_class = serializers.CarFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class UserCarPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarPricing class"""
#
#     queryset = models.CarPricing.objects.all()
#     serializer_class = serializers.CarPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class UserCarReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the CarReview class"""
#
#     queryset = models.CarReview.objects.all()
#     serializer_class = serializers.CarReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerCarViewSet(ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCartList


class CustomerCarDetailsViewSet(ListAPIView):
    queryset = models.CarDetails.objects.all()
    serializer_class = serializers.CarDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerCarFAQViewSet(ListAPIView):
    queryset = models.CarFAQ.objects.all()
    serializer_class = serializers.CarFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerCarPricingViewSet(ListAPIView):
    queryset = models.CarPricing.objects.all()
    serializer_class = serializers.CarPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerCarBookingViewSet(ListCreateAPIView):
    queryset = models.CarBooking.objects.all()
    serializer_class = serializers.CarBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCarBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerCarReviewViewSet(viewsets.ModelViewSet):
    queryset = models.CarReview.objects.all()
    serializer_class = serializers.CarReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterCarReviewViewSet

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car_id = serializer.validated_data.get('car')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_car = models.CarBooking.objects.filter(
            car=car_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_car:
            return Response({"message": "Cannot create a review for an unconfirmed booking."},
                            status=status.HTTP_400_BAD_REQUEST)

        reviewed_car = models.CarReview.objects.filter(
            car=car_id,
            customer=customer_instance).exists()

        if reviewed_car:
            return Response({"message": "Cannot create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(customer=customer_instance)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        car_id = request.data.get('car')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_car = models.CarReview.objects.filter(
            car=car_id,
            customer=customer_instance).exists()

        if not reviewed_car:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_car = models.CarBooking.objects.filter(
            car=car_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_car:
            return Response({"message": "You did not book the car."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     car_id = serializer.validated_data.get('car')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_car = models.CarBooking.objects.filter(
    #         car=car_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #
    #     if not booked_car:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_car = models.CarReview.objects.filter(
    #         car=car_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_car:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)

    # def post(self, request, *args, **kwargs):
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #     serializer = self.serializer_class(data=request.data, context={'request': customer_instance})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
