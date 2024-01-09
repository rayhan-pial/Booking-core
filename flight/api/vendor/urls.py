from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("flight", views.AdminFlightViewSet)
# router.register("FlightBooking", views.FlightBookingAdminViewSet)
router.register("flight-faq", views.AdminFlightFAQViewSet)
router.register("flight-pricing", views.AdminFlightPricingViewSet)
# router.register("FlightReview", views.FlightReviewAdminViewSet)
router.register("flight-seat-type", views.AdminFlightSeatTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-flight-booking/", views.AdminFlightBookingViewSet.as_view()),
    path("admin-flight-booking-update/<int:pk>/", views.AdminFlightBookingUpdateViewsSet.as_view()),
    path("admin-flight-review/", views.AdminFlightReviewViewSet.as_view()),

)