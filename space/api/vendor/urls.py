from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("Space", views.AdminSpaceViewSet)
# router.register("SpaceBooking", views.SpaceBookingAdminViewSet)
router.register("SpaceDetails", views.AdminSpaceDetailsViewSet)
router.register("SpaceFAQ", views.AdminSpaceFAQViewSet)
router.register("SpacePricing", views.AdminSpacePricingViewSet)
# router.register("SpaceReview", views.SpaceReviewAdminViewSet)
router.register("SpaceTicketType", views.AdminSpaceTicketTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-space-booking/", views.AdminSpaceBookingViewSet.as_view()),
    path("admin-space-booking-update/<int:pk>/", views.AdminSpaceBookingUpdateViewsSet.as_view()),
    path("admin-space-review/", views.AdminSpaceReviewViewSet.as_view()),

)