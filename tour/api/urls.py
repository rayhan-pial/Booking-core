from django.urls import path, include

urlpatterns = [
    path("vendor/", include("tour.api.vendor.urls")),
    path("website/", include("tour.api.website.urls"))
]
