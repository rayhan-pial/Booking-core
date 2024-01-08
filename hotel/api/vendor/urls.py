from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("Hotel", views.AdminHotelViewSet)
# router.register("HotelBooking", views.HotelBookingAdminViewSet)
router.register("HotelFAQ", views.AdminHotelFAQViewSet)
router.register("HotelPricing", views.AdminHotelPricingViewSet)
# router.register("HotelReview", views.HotelReviewAdminViewSet)
router.register("HotelRules", views.AdminHotelRulesViewSet)
router.register("Room", views.AdminRoomViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-hotel-booking/", views.AdminHotelBookingViewSet.as_view()),
    path("admin-hotel-booking-update/<int:pk>/", views.AdminHotelBookingUpdateViewsSet.as_view()),
    path("admin-review/", views.AdminHotelReviewViewSet.as_view()),

)