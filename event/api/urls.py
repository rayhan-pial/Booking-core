from django.urls import path, include

urlpatterns = [
    path("vendor/", include("event.api.vendor.urls")),
    path("website/", include("event.api.website.urls"))
]
