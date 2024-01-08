from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.IntegerChoices):
    VENDOR = 0, _('VENDOR')
    CUSTOMER = 1,_('CUSTOMER')