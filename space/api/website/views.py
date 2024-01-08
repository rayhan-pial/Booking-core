from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from . import serializers
from space import models

from django_filters import rest_framework as dj_filters
from space import filters


# class SpaceViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Space class"""
#
#     queryset = models.Space.objects.all()
#     serializer_class = serializers.SpaceSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpaceBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceBooking class"""
#
#     queryset = models.SpaceBooking.objects.all()
#     serializer_class = serializers.SpaceBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpaceDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceDetails class"""
#
#     queryset = models.SpaceDetails.objects.all()
#     serializer_class = serializers.SpaceDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpaceFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceFAQ class"""
#
#     queryset = models.SpaceFAQ.objects.all()
#     serializer_class = serializers.SpaceFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpacePricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpacePricing class"""
#
#     queryset = models.SpacePricing.objects.all()
#     serializer_class = serializers.SpacePricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpaceReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceReview class"""
#
#     queryset = models.SpaceReview.objects.all()
#     serializer_class = serializers.SpaceReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class SpaceTicketTypeViewSet(viewsets.ModelViewSet):
#     """ViewSet for the SpaceTicketType class"""
#
#     queryset = models.SpaceTicketType.objects.all()
#     serializer_class = serializers.SpaceTicketTypeSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerSpaceViewSet(ListAPIView):
    queryset = models.Space.objects.all()
    serializer_class = serializers.SpaceSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceList


class CustomerSpaceBookingViewSet(ListCreateAPIView):
    queryset = models.SpaceBooking.objects.all()
    serializer_class = serializers.SpaceBookingSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceBookingViewSet

    def get(self, request, **kwargs):
        data = self.queryset.filter(customer=self.request.user.customer_user.first())
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()
        serializer.save(customer=customer_instance)


class CustomerCarPricingViewSet(ListAPIView):
    queryset = models.SpacePricing.objects.all()
    serializer_class = serializers.SpacePricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerSpaceDetailsViewSet(ListAPIView):
    queryset = models.SpaceDetails.objects.all()
    serializer_class = serializers.SpaceDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerSpaceFAQViewSet(ListAPIView):
    queryset = models.SpaceFAQ.objects.all()
    serializer_class = serializers.SpaceFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerSpacePricingViewSet(ListAPIView):
    queryset = models.SpacePricing.objects.all()
    serializer_class = serializers.SpacePricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerSpaceReviewViewSet(viewsets.ModelViewSet):
    queryset = models.SpaceReview.objects.all()
    serializer_class = serializers.SpaceReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterSpaceReviewViewSet

    def create(self, request, *args, **kwargs):
        space_id = request.data.get('space')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        booked_space = models.SpaceBooking.objects.filter(
            space=space_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_space:
            return Response({"message": "Have to book first to review"},
                            status=status.HTTP_400_BAD_REQUEST)

        reviewed_space = models.SpaceReview.objects.filter(
            space=space_id,
            customer=customer_instance).exists()

        if reviewed_space:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        space_id = request.data.get('space')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_space = models.SpaceReview.objects.filter(
            space=space_id,
            customer=customer_instance).exists()

        if not reviewed_space:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_space = models.SpaceBooking.objects.filter(
            space=space_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_space:
            return Response({"message": "You did not book the space."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     space_id = serializer.validated_data.get('space')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_space = models.SpaceBooking.objects.filter(
    #         space=space_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #     if not booked_space:
    #         return Response({"message": "Have to book first to review"},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_space = models.SpaceReview.objects.filter(
    #         space=space_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_space:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerSpaceTicketTypeViewSet(ListAPIView):
    queryset = models.SpaceDetails.objects.all()
    serializer_class = serializers.SpaceDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]