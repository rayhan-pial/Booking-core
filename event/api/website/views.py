from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from customer import customer_permissions
from . import serializers
from event import models
from django_filters import rest_framework as dj_filters
from event import filters


# class EventViewSet(viewsets.ModelViewSet):
#     """ViewSet for the Event class"""
#
#     queryset = models.Event.objects.all()
#     serializer_class = serializers.EventSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventBookingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventBooking class"""
#
#     queryset = models.EventBooking.objects.all()
#     serializer_class = serializers.EventBookingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventDetails class"""
#
#     queryset = models.EventDetails.objects.all()
#     serializer_class = serializers.EventDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventFAQViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventFAQ class"""
#
#     queryset = models.EventFAQ.objects.all()
#     serializer_class = serializers.EventFAQSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventPricingViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventPricing class"""
#
#     queryset = models.EventPricing.objects.all()
#     serializer_class = serializers.EventPricingSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventReviewViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventReview class"""
#
#     queryset = models.EventReview.objects.all()
#     serializer_class = serializers.EventReviewSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


# class EventTicketTypeViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventTicketType class"""
#
#     queryset = models.EventTicketType.objects.all()
#     serializer_class = serializers.EventTicketTypeSerializer
#     permission_classes = [customer_permissions.CustomerPermission]


class CustomerEventViewSet(ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterEventList


class CustomerEventBookingViewSet(ListCreateAPIView):
    queryset = models.EventBooking.objects.all()
    serializer_class = serializers.EventBookingSerializer
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


class CustomerEventDetailsViewSet(ListAPIView):
    queryset = models.EventDetails.objects.all()
    serializer_class = serializers.EventDetailsSerializer
    permission_classes = [customer_permissions.CustomerPermission]


# class UserWishlistEventDetailsViewSet(viewsets.ModelViewSet):
#     """ViewSet for the EventDetails class"""
#
#     queryset = models.EventDetails.objects.all()
#     # serializer_class = serializers.WishlistEventDetailsSerializer
#     permission_classes = [customer_permissions.CustomerPermission]
#
#     def get_serializer_class(self):
#         if self.action in ['list', 'retrieve']:
#             return serializers.EventDetailsSerializer
#         else:
#             return serializers.WishlistEventDetailsSerializer


class CustomerEventFAQViewSet(ListAPIView):
    queryset = models.EventFAQ.objects.all()
    serializer_class = serializers.EventFAQSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerEventPricingViewSet(ListAPIView):
    queryset = models.EventPricing.objects.all()
    serializer_class = serializers.EventPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerEventReviewViewSet(viewsets.ModelViewSet):
    queryset = models.EventReview.objects.all()
    serializer_class = serializers.EventReviewSerializer
    permission_classes = [customer_permissions.CustomerPermission]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.FilterEventReviewViewSet

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        user_instance = request.user
        customer_instance = user_instance.customer_user.first()

        booked_event = models.EventBooking.objects.filter(
            event=event_id,
            confirm_booking=True,
            customer=customer_instance
        ).exists()

        if not booked_event:
            return Response({"message": "Have to book first to review"}, status=status.HTTP_400_BAD_REQUEST)

        reviewed_event = models.EventReview.objects.filter(
            event=event_id,
            customer=customer_instance
        ).exists()

        if reviewed_event:
            return Response({"message": "Can't create a new review. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        user_instance = self.request.user
        customer_instance = user_instance.customer_user.first()

        reviewed_event = models.EventReview.objects.filter(
            event=event_id,
            customer=customer_instance).exists()

        if not reviewed_event:
            return Response({"message": "Can't update a new review. First create one."},
                            status=status.HTTP_400_BAD_REQUEST)

        booked_event = models.EventBooking.objects.filter(
            event=event_id,
            confirm_booking=True,
            customer=customer_instance).exists()

        if not booked_event:
            return Response({"message": "You did not book the event."}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        return Response(serializer.data)


    # def perform_create(self, serializer):
    #     event_id = serializer.validated_data.get('event')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     booked_event = models.EventBooking.objects.filter(
    #         event=event_id,
    #         confirm_booking=True,
    #         customer=customer_instance).exists()
    #     if not booked_event:
    #         return Response({"message": "Have to book first to review"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     reviewed_event = models.EventReview.objects.filter(
    #         event=event_id,
    #         customer=customer_instance).exists()
    #
    #     if reviewed_event:
    #         return Response({"message": "Can't create a new review. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)


class CustomerEventTicketTypeViewSet(ListAPIView):
    queryset = models.EventPricing.objects.all()
    serializer_class = serializers.EventPricingSerializer
    permission_classes = [customer_permissions.CustomerPermission]


class CustomerWishlistViewSet(viewsets.ModelViewSet):

    queryset = models.UserWishList.objects.all()
    serializer_class = serializers.UserWishListSerializer
    permission_classes = [customer_permissions.CustomerPermission]

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        user_instance = request.user
        customer_instance = user_instance.customer_user.first()

        wished_event = models.UserWishList.objects.filter(
            event=event_id,
            customer=customer_instance
        ).exists()

        if wished_event:
            return Response({"message": "Can't create a wish for the event. Update the existing one."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer_instance)

        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     event_id = serializer.validated_data.get('event')
    #     user_instance = self.request.user
    #     customer_instance = user_instance.customer_user.first()
    #
    #     wished_event = models.UserWishList.objects.filter(
    #         event=event_id,
    #         customer=customer_instance).exists()
    #
    #     if wished_event:
    #         return Response({"message": "Can't create a wish for the event. Update the existing one."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save(customer=customer_instance)
