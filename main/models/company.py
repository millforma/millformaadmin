from django.contrib.auth.models import User
from django.db import models

from main.models.entity import Entity, EntityAddress
from main.models.phone import Phone


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Company(Entity):
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    contact = models.OneToOneField(

        User, blank=True, null=True, on_delete=models.CASCADE
    )

    adresse = models.ForeignKey(EntityAddress, on_delete=models.CASCADE, blank=True, null=True)
    raison_sociale = models.CharField(max_length=100, default="non renseignee", null=True, blank=True)
    num_decla_activite = models.CharField(max_length=100, default="non renseignee", null=True, blank=True)
    num_siret = models.CharField(max_length=100, default="non renseignee", null=True, blank=True)
    code_ape = models.CharField(max_length=100, default=0, null=True, blank=True)
    email = models.EmailField(max_length=254)
    numb_employees = models.IntegerField(default=0)
    Industry = models.CharField(max_length=100, default="non renseignee", null=True, blank=True)
    phone = models.ForeignKey(Phone, default=None, blank=True, related_name="company_phone",
                              on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

    # Django Models not Showing Up in DB after syncdb
    class Meta:
        app_label = "main"
