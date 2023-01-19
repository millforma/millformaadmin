
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

from main.models import Event
from main.models.address import Address
from main.models.address_type import AddressType
from main.models.company import Company
from main.models.entity import EntityAddress, EntityPhone
from main.models.file.base import BaseFile
from main.models.file.document import DocumentFile
from main.models.file.document_type import DocumentType
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession, Objectifs_peda
from main.models.person import PersonProfession, Person
from main.models.phone import Phone
from main.models.videochat import VideoChat

admin.site.register(EntityAddress)
admin.site.register(Address)
admin.site.register(AddressType)
admin.site.register(DocumentType)
admin.site.register(PersonProfession)
admin.site.register(EntityPhone)
admin.site.register(FormationSession)
admin.site.register(Company)
admin.site.register(PdfDocument)
admin.site.register(VideoChat)
admin.site.register(DocumentFile)
admin.site.register(Phone)
admin.site.register(Event)
admin.site.register(Person)
admin.site.register(Objectifs_peda)


