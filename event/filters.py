from django_filters import rest_framework as dj_filters


from event import  models


class FilterEventList(dj_filters.FilterSet):

    class Meta:
        model = models.Event
        fields = ('average_rating', 'is_active', 'pricing_event__price')


class FilterBoatBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.EventBooking
        fields = ('star_date', 'confirm_booking', 'total_cost', )


class FilterEventReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.EventReview
        fields = ('rating', 'review_time', )


# class FilterCustomerBoatSpecsViewSet(dj_filters.FilterSet):
#
#     class Meta:
#         model = models.BoatSpecs
#         fields = ('rating', 'review_time', )
