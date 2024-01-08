from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("Tour", views.AdminTourViewSet)
# router.register("TourBooking", views.TourBookingAdminViewSet)
router.register("TourDetails", views.AdminTourDetailsViewSet)
router.register("TourFAQ", views.AdminTourFAQViewSet)
router.register("TourItinerary", views.AdminTourItineraryViewSet)
router.register("TourPricing", views.AdminTourPricingViewSet)
# router.register("TourReview", views.TourReviewAdminViewSet)
router.register("TourRules", views.AdminTourRulesViewSet)
router.register("TourTicketType", views.AdminTourTicketTypeViewSet)

urlpatterns = [
    path("admin/", include(router.urls)),
    path("admin-tour-booking/", views.AdminTourBookingViewSet.as_view()),
    path("admin-tour-booking-update/<int:pk>/", views.AdminTourBookingUpdateViewsSet.as_view()),
    path("admin-tour-review/", views.AdminTourReviewViewSet.as_view()),
]