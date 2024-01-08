from django.urls import path, include

urlpatterns = [
    path("vendor/", include("flight.api.vendor.urls")),
    path("website/", include("flight.api.website.urls"))
]
