import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from main.models.address import Address
from main.models.base import BaseModel
from main.models.company import Company

from main.models.person import Person



class FormationSession(BaseModel):
    OPCO_SANTE = 1
    OPCO2i = 2
    OPCO_MOBILITES = 3
    OPCO_EP = 4
    OPCO_COMMERCE = 5
    AKTO = 6
    OCAPIAT = 7
    AFDAS = 8
    ATLAS = 9
    UNIFORMATION = 10
    CONSTRUCTYS = 11

    OPCO_NAMES_CHOICES = [
        (OPCO_SANTE, "OpcoSanté"),
        (OPCO2i, "Opco2I"),
        (OPCO_MOBILITES, "OpcoMobilités"),
        (OPCO_EP, "OpcoEp"),
        (OPCO_COMMERCE, "OpCommerce"),
        (AKTO, "Akto"),
        (OCAPIAT, "Ocapiat"),
        (AFDAS, "Afdas"),
        (ATLAS, "Atlas"),
        (UNIFORMATION, "Uniformation"),
        (CONSTRUCTYS, "Constructys"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    commercial = models.ForeignKey(to=User, limit_choices_to={'groups__name': "commercial"},
                                   on_delete=models.DO_NOTHING, related_name="commercial")

    name = models.CharField(max_length=200)
    trainee = models.ManyToManyField(Person)
    num_present_trainee = models.IntegerField(default=0)
    doc_has_been_sent = models.BooleanField(default=False)
    foad = models.BooleanField(default=False)
    training_site = models.ForeignKey(to=Address, on_delete=models.DO_NOTHING)
    prerequis_formation = models.BooleanField(default=False)
    completed_videochat_sessions = models.IntegerField(default=0, null=True, blank=True)

    teacher_name = models.ForeignKey(to=User, limit_choices_to={'groups__name': "teacher"}, on_delete=models.DO_NOTHING)
    opco_name = models.IntegerField(choices=OPCO_NAMES_CHOICES, default=1)
    date_autorised_start = models.DateField(auto_now=False, auto_now_add=False)
    date_autorised_end = models.DateField(auto_now=False, auto_now_add=False)
    date_start = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    date_end = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    training_duration = models.IntegerField(default=0)
    training_done = models.IntegerField(default=0, null=True, blank=True)
    is_finished=models.BooleanField(default=False)
    client_account = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    old_num_formation = models.CharField(max_length=35, default="DC-00000")
    date_creation_formation = models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(FormationSession, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"



