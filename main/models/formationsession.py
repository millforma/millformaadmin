import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from main.models.address import Address
from main.models.base import BaseModel
from main.models.company import Company

from main.models.person import Person



class FormationSession(BaseModel):

    AKTO_Reseau_Fafih = 1
    AFDAS = 2
    AFDAS_Intermittent = 3
    OPCO_ATLAS = 4
    CAISSE_DES_DEPOTS_ET_CONSIGNATIONS = 5
    OPCALIA = 6
    AGEFICE = 7
    FP = 8
    AKTO_Reseau_Intergros = 9
    OPCOMMERCE = 10
    OPCO_EP = 11
    OPCOmobilite = 12
    OCAPIAT = 13
    OPCO_2I = 14

    OPCO_NAMES_CHOICES = [
        (AKTO_Reseau_Fafih, "AKTO Réseau Fafih"),
        (AFDAS, "AFDAS"),
        (AFDAS_Intermittent, "AFDAS (Intermittent)"),
        (OPCO_ATLAS, "OPCO ATLAS"),
        (CAISSE_DES_DEPOTS_ET_CONSIGNATIONS, "CAISSE DES DEPOTS ET CONSIGNATIONS"),
        (OPCALIA, "OPCALIA"),
        (AGEFICE, "AGEFICE"),
        (FP, "FP"),
        (AKTO_Reseau_Intergros, "AKTO Réseau Intergros"),
        (OPCOMMERCE, "OPCOMMERCE"),
        (OPCO_EP, "OPCO EP"),
        (OPCOmobilite, "OPCOmobilité"),
        (OCAPIAT, "OCAPIAT"),
        (OPCO_2I, "OPCO 2I"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    commercial = models.ForeignKey(to=User, limit_choices_to={'groups__name': "commercial"},
                                   on_delete=models.DO_NOTHING, related_name="commercial", blank=True,null=True)
    name = models.CharField(max_length=200)
    trainee = models.ManyToManyField(Person,blank=True, null=True)
    num_present_trainee = models.IntegerField(default=0)
    doc_has_been_sent = models.BooleanField(default=False)
    foad = models.BooleanField(default=False)
    training_site = models.ForeignKey(to=Address, on_delete=models.DO_NOTHING, blank=True,null=True)
    prerequis_formation = models.BooleanField(default=False)
    completed_videochat_sessions = models.IntegerField(default=0, null=True, blank=True)
    teacher_name = models.ForeignKey(to=User, limit_choices_to={'groups__name': "teacher"}, on_delete=models.DO_NOTHING, blank=True,null=True)
    opco_name = models.IntegerField(choices=OPCO_NAMES_CHOICES, default=1)
    date_autorised_start = models.DateField(auto_now=False, auto_now_add=False)
    date_autorised_end = models.DateField(auto_now=False, auto_now_add=False)
    date_start = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    date_end = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    training_duration = models.IntegerField(default=0)
    training_done = models.IntegerField(default=0, null=True, blank=True)
    is_finished=models.BooleanField(default=False)
    client_account = models.ForeignKey(to=Company, on_delete=models.DO_NOTHING, blank=True,null=True)
    old_num_formation = models.CharField(max_length=35, default="DC-00000")
    date_creation_formation = models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(FormationSession, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"



