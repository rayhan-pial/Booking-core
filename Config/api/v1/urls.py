from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('auth/', include('coreapp.api.urls')),
    path('utility/', include('utility.api.urls')),
    path('boat/', include('boat.api.urls')),
    path('car/', include('car.api.urls')),
    path('customer/', include('customer.api.urls')),
    path('event/', include('event.api.urls')),
    path('flight/', include('flight.api.urls')),
    path('hotel/', include('hotel.api.urls')),
    path('space/', include('space.api.urls')),
    path('tour/', include('tour.api.urls')),
    path('vendor/', include('vendor.api.urls')),
]
