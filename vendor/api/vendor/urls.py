from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register("vendor", views.vendorViewSet)

urlpatterns = (
    path("route/", include(router.urls)),
)