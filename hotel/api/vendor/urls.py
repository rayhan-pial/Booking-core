from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("hotel", views.AdminHotelViewSet)
# router.register("HotelBooking", views.HotelBookingAdminViewSet)
router.register("hotel-faq", views.AdminHotelFAQViewSet)
router.register("hotel-pricing", views.AdminHotelPricingViewSet)
# router.register("HotelReview", views.HotelReviewAdminViewSet)
router.register("hotel-rules", views.AdminHotelRulesViewSet)
router.register("room", views.AdminRoomViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-hotel-booking/", views.AdminHotelBookingViewSet.as_view()),
    path("admin-hotel-booking-update/<int:pk>/", views.AdminHotelBookingUpdateViewsSet.as_view()),
    path("admin-review/", views.AdminHotelReviewViewSet.as_view()),

)