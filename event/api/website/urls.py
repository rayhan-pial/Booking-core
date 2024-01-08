from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register("Event", views.EventViewSet)
# router.register("EventBooking", views.EventBookingViewSet)
# router.register("EventDetails", views.EventDetailsViewSet)
# router.register("EventFAQ", views.EventFAQViewSet)
# router.register("EventPricing", views.EventPricingViewSet)
# router.register("EventReview", views.EventReviewViewSet)
# router.register("EventTicketType", views.EventTicketTypeViewSet)
router.register("wish-list", views.CustomerWishlistViewSet)
router.register("review", views.CustomerEventReviewViewSet)

urlpatterns = (
    path("user-event-/", include(router.urls)),
    path("user-event-view/", views.CustomerEventViewSet.as_view()),
    path("user-event-booking/", views.CustomerEventBookingViewSet.as_view()),
    path("user-event-details/", views.CustomerEventDetailsViewSet.as_view()),
    path("user-event-faq/", views.CustomerEventFAQViewSet.as_view()),
    path("user-event-pricing/", views.CustomerEventPricingViewSet.as_view()),
    # path("user-event-review/", views.CustomerEventReviewViewSet.as_view()),
    path("user-event-ticket-type/", views.CustomerEventTicketTypeViewSet.as_view()),

)