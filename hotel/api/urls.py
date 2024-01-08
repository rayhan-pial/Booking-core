from django.urls import path, include

urlpatterns = [
    path("vendor/", include("hotel.api.vendor.urls")),
    path("website/", include("hotel.api.website.urls"))
]
