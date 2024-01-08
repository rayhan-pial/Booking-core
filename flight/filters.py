from django_filters import rest_framework as dj_filters


from flight import models


class FilterFlightList(dj_filters.FilterSet):

    class Meta:
        model = models.Flight
        fields = ('average_rating', 'is_active', 'departure_time', 'arrival_time', 'arrival_location',
                  'departure_location', 'pricing_flight__price', )


class FilterFlightBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.FlightBooking
        fields = ('confirm_booking', 'total_cost', )


class FilterFlightReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.FlightReview
        fields = ('rating', 'review_time', )


# class FilterCustomerBoatSpecsViewSet(dj_filters.FilterSet):
#
#     class Meta:
#         model = models.BoatSpecs
#         fields = ('rating', 'review_time', )
