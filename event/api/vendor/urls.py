from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("event", views.AdminEventViewSet)
# router.register("EventBooking", views.EventBookingAdminViewSet)
router.register("event-details", views.AdminEventDetailsViewSet)
router.register("event-fAQ", views.AdminEventFAQViewSet)
router.register("event-pricing", views.AdminEventPricingViewSet)
# router.register("EventReview", views.EventReviewAdminViewSet)
router.register("event-ticket-type", views.AdminEventTicketTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-event-booking/", views.AdminEventBookingViewSet.as_view()),
    path("admin-event-booking_update/<int:pk>/", views.AdminEventBookingUpdateViewsSet.as_view()),
    path("admin-event-review/", views.AdminEventBookingViewSet.as_view()),

)