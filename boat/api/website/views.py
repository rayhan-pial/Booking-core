from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from . import serializers
from boat import models
from customer import customer_permissions
from vendor import vendor_permissions
from django_filters import rest_framework as dj_filters
from boat import filters


# class BoatViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Boat class"""
#
#     queryset = models.Boat.objects.all()
#     serializer_class = serializers.BoatSerializer
#     permission_classes = [customer_permissions.CustomerPermission, ]


# class BoatBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatBooking class"""
#
#     queryset = models.BoatBooking.objects.all()
#     serializer_class = serializers.BoatBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatDetails class"""
#
#     queryset = models.BoatDetails.objects.all()
#     serializer_class = serializers.BoatDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatFAQ class"""
#
#     queryset = models.BoatFAQ.objects.all()
#     serializer_class = serializers.BoatFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatPricing class"""
#
#     queryset = models.BoatPricing.objects.all()
#     serializer_class = serializers.BoatPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatReview class"""
#
#     queryset = models.BoatReview.objects.all()
#     serializer_class = serializers.BoatReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatSpecsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatSpecs class"""
#
#     queryset = models.BoatSpecs.objects.all()
#     serializer_class = serializers.BoatSpecsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class BoatTicketTypeViewSet(viewsets.ModelViewSet):
#     """ViewSet for the BoatTicketType class"""
#
#     queryset = models.BoatTicketType.objects.all()
#     serializer_class = serializers.BoatTicketTypeSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerBoatViewSet(ListAPIView):
    queryset = models.Boat.objects.all()
    serializer_class = serializers.BoatSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatList


class CustomerBoatBookingViewSet(ListCreateAPIView):
    queryset = models.BoatBooking.objects.all()
    serializer_class = serializers.BoatBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerBoatDetailsViewSet(ListAPIView):
    queryset = models.BoatDetails.objects.all()
    serializer_class = serializers.BoatDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatDetailsViewSet


class CustomerBoatFAQViewSet(ListAPIView):
    queryset = models.BoatFAQ.objects.all()
    serializer_class = serializers.BoatFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerBoatPricingViewSet(ListAPIView):
    queryset = models.BoatPricing.objects.all()
    serializer_class = serializers.BoatPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerBoatReviewViewSet(viewsets.ModelViewSet):
    queryset = models.BoatReview.objects.all()
    serializer_class = serializers.BoatReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterBoatReviewViewSet

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        boat_id = serializer.validated_data.get('boat')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_boat = models.BoatBooking.objects.filter(
            boat=boat_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_boat:
            return Response({"message": "You did not book the boat."}, status=status.HTTP_400_BAD_REQUEST)

        reviewed_boat = models.BoatReview.objects.filter(
            boat=boat_id,
            customer=customer_instance).exists()

        if reviewed_boat:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(customer=customer_instance)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        boat_id = request.data.get('boat')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_boat = models.BoatReview.objects.filter(
            boat=boat_id,
            customer=customer_instance).exists()

        if not reviewed_boat:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_boat = models.BoatBooking.objects.filter(
            boat=boat_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_boat:
            return Response({"message": "You did not book the boat."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     boat_id = serializer.validated_data.get('boat')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_boat = models.BoatBooking.objects.filter(
    #         boat=boat_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #
    #     if not booked_boat:
    #         return Response({"message": "You did not book the boat."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_boat = models.BoatReview.objects.filter(
    #         boat=boat_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_boat:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerBoatSpecsViewSet(ListAPIView):
    queryset = models.BoatSpecs.objects.all()
    serializer_class = serializers.BoatSpecsSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerBoatTicketTypeViewSet(ListAPIView):
    queryset = models.BoatTicketType.objects.all()
    serializer_class = serializers.BoatTicketTypeSerializer
    permission_classes = [customer_permissions.CustomerPermission]
