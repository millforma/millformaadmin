from django.contrib.auth.models import User
from django.db import models
from jsignature.mixins import JSignatureFieldsMixin

from main.models.file.pdf_document import PdfDocument


class SignatureModel(JSignatureFieldsMixin):
    signature_owner = models.ForeignKey(to=User,on_delete=models.DO_NOTHING,
                                        related_name="signature_owner", blank=True, null=True)