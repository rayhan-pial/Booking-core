from django_filters import rest_framework as dj_filters


from boat.models import Boat, BoatBooking, BoatDetails, BoatReview


class FilterBoatList(dj_filters.FilterSet):

    class Meta:
        model = Boat
        fields = ('average_rating', 'is_active', 'pricing_boat__price', )


class FilterBoatBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = BoatBooking
        fields = ('star_date', 'end_date', 'confirm_booking', 'total_cost', 'total_time', )


class FilterBoatDetailsViewSet(dj_filters.FilterSet):

    class Meta:
        model = BoatDetails
        fields = ('cabin', 'max_guest', 'speed', 'length', )


class FilterBoatReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = BoatReview
        fields = ('rating', 'review_time', )


# class FilterCustomerBoatSpecsViewSet(dj_filters.FilterSet):
#
#     class Meta:
#         model = models.BoatSpecs
#         fields = ('rating', 'review_time', )
