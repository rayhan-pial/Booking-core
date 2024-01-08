from django_filters import rest_framework as dj_filters


from hotel import models


class FilterHotelList(dj_filters.FilterSet):

    class Meta:
        model = models.Hotel
        fields = ('average_rating', 'is_active', 'hotel_star', 'pricing_hotel__price', )


class FilterHotelBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.HotelBooking
        fields = ('check_in', 'check_out', 'confirm_booking', 'total_cost', )


class FilterHotelReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.HotelReview
        fields = ('rating', 'review_time', )
