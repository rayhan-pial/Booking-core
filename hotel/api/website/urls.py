from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register("Hotel", views.HotelViewSet)
# router.register("HotelBooking", views.HotelBookingViewSet)
# router.register("HotelFAQ", views.HotelFAQViewSet)
# router.register("HotelPricing", views.HotelPricingViewSet)
# router.register("HotelReview", views.HotelReviewViewSet)
# router.register("HotelRules", views.HotelRulesViewSet)
# router.register("Room", views.RoomViewSet)
router.register("HotelReview", views.CustomerHotelReviewViewSet)

urlpatterns = (
    path("website/", include(router.urls)),
    path("user-hotel-list/", views.CustomerHotelViewSet.as_view()),
    path("user-hotel-booking/", views.CustomerHotelBookingViewSet.as_view()),
    path("user-hotel-faq/", views.CustomerHotelFAQViewSet.as_view()),
    path("user-hotel-pricing/", views.CustomerHotelPricingViewSet.as_view()),
    # path("user-hotel-review/", views.CustomerHotelReviewViewSet.as_view()),
    path("user-hotel-rules/", views.CustomerHotelRulesViewSet.as_view()),
    path("user-hotel-room/", views.CustomerRoomViewSet.as_view()),

)