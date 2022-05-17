from django.db import models
from jsignature.mixins import JSignatureFieldsMixin

from main.models.file.pdf_document import PdfDocument


class SignatureModel(JSignatureFieldsMixin):
    doc=models.ForeignKey(to=PdfDocument, on_delete=models.DO_NOTHING)