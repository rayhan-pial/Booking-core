from django.urls import path, include

urlpatterns = [
    path("vendor/", include("customer.api.vendor.urls")),
    path("website/", include("customer.api.website.urls"))
]
