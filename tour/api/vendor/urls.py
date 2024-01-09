from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("tour", views.AdminTourViewSet)
# router.register("TourBooking", views.TourBookingAdminViewSet)
router.register("tour-details", views.AdminTourDetailsViewSet)
router.register("tour-faq", views.AdminTourFAQViewSet)
router.register("tour-itinerary", views.AdminTourItineraryViewSet)
router.register("tour-pricing", views.AdminTourPricingViewSet)
# router.register("TourReview", views.TourReviewAdminViewSet)
router.register("tour-rules", views.AdminTourRulesViewSet)
router.register("tour-ticket-type", views.AdminTourTicketTypeViewSet)

urlpatterns = [
    path("admin/", include(router.urls)),
    path("admin-tour-booking/", views.AdminTourBookingViewSet.as_view()),
    path("admin-tour-booking-update/<int:pk>/", views.AdminTourBookingUpdateViewsSet.as_view()),
    path("admin-tour-review/", views.AdminTourReviewViewSet.as_view()),
]