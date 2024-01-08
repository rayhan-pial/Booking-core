from django_filters import rest_framework as dj_filters


from car import models


class FilterCartList(dj_filters.FilterSet):

    class Meta:
        model = models.Car
        fields = ('average_rating', 'is_active', 'pricing_car__price', )


class FilterCarBookingViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.CarBooking
        fields = ('star_date', 'end_date', 'confirm_booking', 'total_cost', )


# class FilterCarDetailsViewSet(dj_filters.FilterSet):
#
#     class Meta:
#         model = BoatDetails
#         fields = ('cabin', 'max_guest', 'speed', 'length', )


class FilterCarReviewViewSet(dj_filters.FilterSet):

    class Meta:
        model = models.CarReview
        fields = ('rating', 'review_time', )


# class FilterCustomerBoatSpecsViewSet(dj_filters.FilterSet):
#
#     class Meta:
#         model = models.BoatSpecs
#         fields = ('rating', 'review_time', )
