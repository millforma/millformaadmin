from django.contrib.auth.models import User
from .document import DocumentFile
from django.db import models
from .document_type import DocumentType
from ..formationsession import FormationSession


class PdfDocument(DocumentFile):
    formation_session=models.ForeignKey(to=FormationSession,on_delete=models.DO_NOTHING)
    is_signed=models.BooleanField(default=False)
    is_signed_by=models.ManyToManyField(User,related_name="signed_by")
    numb_of_signed_trainees=models.IntegerField(default=0)
    verification_code=models.IntegerField(default=1658)
    type_of_document=models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, blank=True, null=True,default=None
    )