from django_filters import rest_framework as dj_filters


from space import models


class FilterSpaceList(dj_filters.FilterSet):

    class Meta:
        model = models.Space
        fields = ('average_rating', 'is_active', 'pricing_space__price', )


class FilterSpaceBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.SpaceBooking
        fields = ('star_date', 'end_date', 'confirm_booking', 'total_cost', )


class FilterSpaceReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.SpaceReview
        fields = ('rating', 'review_time', )

