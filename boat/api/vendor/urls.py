from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("boat", views.BoatAdminViewSet)
# router.register("BoatBooking", views.BoatBookingAdminViewSet)
router.register("boat-details", views.AdminBoatDetailsViewSet)
router.register("boat-fAQ", views.AdminBoatFAQViewSet)
router.register("boat-pricing", views.AdminBoatPricingViewSet)
# router.register("BoatReview", views.BoatReviewAdminViewSet)
router.register("boat-specs", views.AdminBoatSpecsViewSet)
router.register("boat-ticket-type", views.AdminBoatTicketTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-boat-bookings/", views.AdminBoatBookingViewSet.as_view()),
    path("admin-boat-booking-update/<int:pk>/", views.AdminBoatBookingUpdateViewsSet.as_view()),
    path("admin-boat-review/", views.AdminBoatReviewViewSet.as_view()),

)
