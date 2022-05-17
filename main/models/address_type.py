from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models.base import BaseModel


class AddressType(BaseModel):
    ADDRESS_TYPES_HOME = 1
    ADDRESS_TYPES_WORK = 2
    ADDRESS_TYPES = {
        ADDRESS_TYPES_HOME: _("Home"),
        ADDRESS_TYPES_WORK: _("Work"),
    }
    name = models.IntegerField(
        blank=False,
        null=False,
        default=ADDRESS_TYPES_HOME,
        choices=[(k, v) for k, v in ADDRESS_TYPES.items()],
    )

    def __str__(self):
        return str(self.ADDRESS_TYPES[(self.name)])
