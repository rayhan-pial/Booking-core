from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("car", views.AdminCarViewSet)
# router.register("CarBooking", views.CarBookingAdminViewSet)
router.register("car-details", views.AdminCarDetailsViewSet)
router.register("car-fAQ", views.AdminCarFAQViewSet)
router.register("car-pricing", views.AdminCarPricingViewSet)
# router.register("CarReview", views.CarReviewAdminViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-car-booking/", views.AdminCarBookingViewSet.as_view()),
    path("admin-car-review/", views.AdminCarReviewViewSet.as_view()),
    path("admin-car-booking_update/<int:pk>/", views.AdminCarBookingUpdateViewsSet.as_view()),
)
