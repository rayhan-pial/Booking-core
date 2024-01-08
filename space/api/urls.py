from django.urls import path, include

urlpatterns = [
    path("vendor/", include("space.api.vendor.urls")),
    path("website/", include("space.api.website.urls"))
]
