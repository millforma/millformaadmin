
from django.contrib import admin

from main.models.address import Address
from main.models.address_type import AddressType
from main.models.company import Company
from main.models.entity import EntityAddress, EntityPhone
from main.models.formationsession import FormationSession
from main.models.person import PersonProfession

admin.site.register(EntityAddress)
admin.site.register(Address)
admin.site.register(AddressType)
admin.site.register(PersonProfession)
admin.site.register(EntityPhone)
admin.site.register(FormationSession)
admin.site.register(Company)
