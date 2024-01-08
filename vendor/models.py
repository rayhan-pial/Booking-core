from django.db import models
from django.urls import reverse
from django.conf import settings
from coreapp.base import BaseModel


class vendor(BaseModel):
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_user")

    # Fields
    location = models.CharField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("vendor_vendor_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("vendor_vendor_update", args=(self.pk,))
