
from django.contrib import admin
from django.apps import apps
from main.models.address import Address
from main.models.address_type import AddressType
from main.models.company import Company
from main.models.entity import EntityAddress, EntityPhone
from main.models.file.base import BaseFile
from main.models.file.document import DocumentFile
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession
from main.models.person import PersonProfession
from main.models.videochat import VideoChat

admin.site.register(EntityAddress)
admin.site.register(Address)
admin.site.register(AddressType)
admin.site.register(PersonProfession)
admin.site.register(EntityPhone)
admin.site.register(FormationSession)
admin.site.register(Company)
admin.site.register(PdfDocument)
admin.site.register(VideoChat)
admin.site.register(DocumentFile)

# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
