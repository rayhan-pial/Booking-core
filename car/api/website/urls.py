from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register("Car", views.UserCarViewSet)
# router.register("CarBooking", views.UserCarBookingViewSet)
# router.register("CarDetails", views.UserCarDetailsViewSet)
# router.register("CarFAQ", views.UserCarFAQViewSet)
# router.register("CarPricing", views.UserCarPricingViewSet)
# router.register("CarReview", views.UserCarReviewViewSet)
router.register("CarReview", views.CustomerCarReviewViewSet)

urlpatterns = [
    path("route/", include(router.urls)),
    path("car-list/", views.CustomerCarViewSet.as_view()),
    path("car-details/", views.CustomerCarDetailsViewSet.as_view()),
    path("car-faq/", views.CustomerCarFAQViewSet.as_view()),
    path("car-pricing/", views.CustomerCarPricingViewSet.as_view()),
    path("car-booking/", views.CustomerCarBookingViewSet.as_view()),
    # path("car-review/", views.CustomerCarReviewViewSet.as_view()),
]
