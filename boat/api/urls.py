from django.urls import path, include

urlpatterns = [
    path("vendor/", include("boat.api.vendor.urls")),
    path("website/", include("boat.api.website.urls"))
]
