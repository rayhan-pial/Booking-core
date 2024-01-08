from django.db import models
from django.urls import reverse
from coreapp.base import BaseModel
from django.conf import settings


class Customer(BaseModel):
    # Relationships
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_user")
    # Fields
    location = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.user.first_name)

    def get_absolute_url(self):
        return reverse("customer_customer_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("customer_customer_update", args=(self.pk,))
