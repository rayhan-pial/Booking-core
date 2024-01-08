from django.urls import path, include

urlpatterns = [
    path("vendor/", include("car.api.vendor.urls")),
    path("website/", include("car.api.website.urls"))
]
