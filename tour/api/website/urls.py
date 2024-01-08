from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register("Tour", views.TourViewSet)
# router.register("TourBooking", views.TourBookingViewSet)
# router.register("TourDetails", views.TourDetailsViewSet)
# router.register("TourFAQ", views.TourFAQViewSet)
# router.register("TourItinerary", views.TourItineraryViewSet)
# router.register("TourPricing", views.TourPricingViewSet)
# router.register("TourReview", views.TourReviewViewSet)
# router.register("TourRules", views.TourRulesViewSet)
# router.register("TourTicketType", views.TourTicketTypeViewSet)
router.register("TourReview", views.CustomerTourReviewViewSet)

urlpatterns = (
    path("website/", include(router.urls)),
    path("user-tour-list/", views.CustomerTourViewSet.as_view()),
    path("user-tour-booking/", views.CustomerTourBookingViewSet.as_view()),
    path("user-tour-details/", views.CustomerTourDetailsViewSet.as_view()),
    path("user-tour-faq/", views.CustomerTourFAQViewSet.as_view()),
    path("user-tour-itinerary/", views.CustomerTourItineraryViewSet.as_view()),
    path("user-tour-pricing/", views.CustomerTourPricingViewSet.as_view()),
    # path("user-tour-review/", views.CustomerTourReviewViewSet.as_view()),
    path("user-tour-rules/", views.CustomerTourRulesViewSet.as_view()),
    path("user-tour-ticket-type/", views.CustomerTourTicketTypeViewSet.as_view()),

)