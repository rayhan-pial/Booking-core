from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("Event", views.AdminEventViewSet)
# router.register("EventBooking", views.EventBookingAdminViewSet)
router.register("EventDetails", views.AdminEventDetailsViewSet)
router.register("EventFAQ", views.AdminEventFAQViewSet)
router.register("EventPricing", views.AdminEventPricingViewSet)
# router.register("EventReview", views.EventReviewAdminViewSet)
router.register("EventTicketType", views.AdminEventTicketTypeViewSet)

urlpatterns = (
    path("admin/", include(router.urls)),
    path("admin-event-booking/", views.AdminEventBookingViewSet.as_view()),
    path("admin-event-booking_update/<int:pk>/", views.AdminEventBookingUpdateViewsSet.as_view()),
    path("admin-event-review/", views.AdminEventBookingViewSet.as_view()),

)