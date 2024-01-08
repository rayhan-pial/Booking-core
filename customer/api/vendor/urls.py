from django.urls import path
from django.views import View


class PlaceholderView(View):
    def get(self, request, *args, **kwargs):
        # You can leave this method empty if you don't need any logic
        pass


urlpatterns = [
    path('about/', PlaceholderView.as_view(), name='about'),
    path('contact/', PlaceholderView.as_view(), name='contact'),
    # Add more paths as needed
]
