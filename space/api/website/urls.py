from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register("Space", views.SpaceViewSet)
# router.register("SpaceBooking", views.SpaceBookingViewSet)
# router.register("SpaceDetails", views.SpaceDetailsViewSet)
# router.register("SpaceFAQ", views.SpaceFAQViewSet)
# router.register("SpacePricing", views.SpacePricingViewSet)
# router.register("SpaceReview", views.SpaceReviewViewSet)
# router.register("SpaceTicketType", views.SpaceTicketTypeViewSet)
router.register("SpaceReview", views.CustomerSpaceReviewViewSet)

urlpatterns = (
    path("website/", include(router.urls)),
    path("user-space-list/", views.CustomerSpaceViewSet.as_view()),
    path("user-space-booking/", views.CustomerSpaceBookingViewSet.as_view()),
    path("user-space-details/", views.CustomerSpaceDetailsViewSet.as_view()),
    path("user-space-faq/", views.CustomerSpaceFAQViewSet.as_view()),
    path("user-space-pricing/", views.CustomerSpacePricingViewSet.as_view()),
    # path("user-space-review/", views.CustomerSpaceReviewViewSet.as_view()),
    path("user-space-ticket/", views.CustomerSpaceTicketTypeViewSet.as_view()),

)