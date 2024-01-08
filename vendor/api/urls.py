from django.urls import path, include

urlpatterns = [
    path("vendor/", include("vendor.api.vendor.urls")),
]
