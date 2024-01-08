from django_filters import rest_framework as dj_filters


from tour import models


class FilterTourList(dj_filters.FilterSet):

    class Meta:
        model = models.Tour
        fields = ('average_rating', 'is_active', 'pricing_tour__price', )


class FilterTourBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.TourBooking
        fields = ('star_date', 'confirm_booking', 'total_cost', )


class FilterTourReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.TourReview
        fields = ('rating', 'review_time', )

