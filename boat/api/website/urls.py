from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register("Boat", views.BoatViewSet)
# router.register("BoatBooking", views.BoatBookingViewSet)
# router.register("BoatDetails", views.BoatDetailsViewSet)
# router.register("BoatFAQ", views.BoatFAQViewSet)
# router.register("BoatPricing", views.BoatPricingViewSet)
# router.register("BoatReview", views.BoatReviewViewSet)
# router.register("BoatSpecs", views.BoatSpecsViewSet)
# router.register("BoatTicketType", views.BoatTicketTypeViewSet)
router.register("BoatReview", views.CustomerBoatReviewViewSet)

urlpatterns = (
    path("website/", include(router.urls)),
    path("user-boat-list/", views.CustomerBoatViewSet.as_view()),
    path("user-boat-booking/", views.CustomerBoatBookingViewSet.as_view()),
    path("user-boat-details/", views.CustomerBoatDetailsViewSet.as_view()),
    path("user-boat-faq/", views.CustomerBoatFAQViewSet.as_view()),
    path("user-boat-pricing/", views.CustomerBoatPricingViewSet.as_view()),
    # path("user-boat-review/", views.CustomerBoatReviewViewSet.as_view()),
    path("user-boat-spec/", views.CustomerBoatSpecsViewSet.as_view()),
    path("user-boat-ticket-type/", views.CustomerBoatTicketTypeViewSet.as_view()),

)
