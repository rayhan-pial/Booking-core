from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("Boat", views.BoatAdminViewSet)
# router.register("BoatBooking", views.BoatBookingAdminViewSet)
router.register("BoatDetails", views.AdminBoatDetailsViewSet)
router.register("BoatFAQ", views.AdminBoatFAQViewSet)
router.register("BoatPricing", views.AdminBoatPricingViewSet)
# router.register("BoatReview", views.BoatReviewAdminViewSet)
router.register("BoatSpecs", views.AdminBoatSpecsViewSet)
router.register("BoatTicketType", views.AdminBoatTicketTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-boat-bookings/", views.AdminBoatBookingViewSet.as_view()),
    path("admin-boat-booking-update/<int:pk>/", views.AdminBoatBookingUpdateViewsSet.as_view()),
    path("admin-boat-review/", views.AdminBoatReviewViewSet.as_view()),

)
