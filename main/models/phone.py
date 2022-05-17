import phonenumbers
from django.conf import settings
from django.db import models

from main.models.base import BaseModel


class Phone(BaseModel):
    phone_number = models.TextField(blank=False, null=False)

    @staticmethod
    def standardize(phone_number):
        return phonenumbers.format_number(
            phonenumbers.parse(phone_number, settings.PHONE_ACCEPTED_FORMAT),
            phonenumbers.PhoneNumberFormat.E164,
        )

    def save(self, *args, **kwargs):
        if self.phone_number is not None:
            self.phone_number = self.standardize(self.phone_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number}"
