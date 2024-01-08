from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register("Flight", views.FlightViewSet)
# router.register("FlightBooking", views.FlightBookingViewSet)
# router.register("FlightFAQ", views.FlightFAQViewSet)
# router.register("FlightPricing", views.FlightPricingViewSet)
# router.register("FlightReview", views.FlightReviewViewSet)
# router.register("FlightSeatType", views.FlightSeatTypeViewSet)
router.register("FlightReview", views.CustomerFlightReviewViewSet)

urlpatterns = (
    path("website/", include(router.urls)),
    path("user-flight-list/", views.CustomerFlightViewSet.as_view()),
    path("user-flight-booking/", views.CustomerFlightBookingViewSet.as_view()),
    path("user-flight-faq/", views.CustomerFlightFAQViewSet.as_view()),
    path("user-flight-pricing/", views.CustomerFlightPricingViewSet.as_view()),
    # path("user-flight-review/", views.CustomerFlightReviewViewSet.as_view()),
    path("user-flight-seat/", views.CustomerFlightSeatTypeViewSet.as_view()),

)