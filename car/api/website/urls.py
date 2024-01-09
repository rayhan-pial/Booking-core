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
router.register("car-review", views.CustomerCarReviewViewSet)

urlpatterns = [
    path("user/", include(router.urls)),
    path("user-car-list/", views.CustomerCarViewSet.as_view()),
    path("user-car-details/", views.CustomerCarDetailsViewSet.as_view()),
    path("user-car-faq/", views.CustomerCarFAQViewSet.as_view()),
    path("user-car-pricing/", views.CustomerCarPricingViewSet.as_view()),
    path("user-car-booking/", views.CustomerCarBookingViewSet.as_view()),
    # path("car-review/", views.CustomerCarReviewViewSet.as_view()),
]
