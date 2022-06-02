from django.db import models
from django.utils.functional import cached_property

from main.models.file.base import BaseFile
from django.conf import settings

from main.models.file.document_type import DocumentType


class DocumentFile(BaseFile):


    actual_file = models.FileField(
        default=None,
        null=True,
        blank=True,
        upload_to=BaseFile.generate_filename,
    )
    type=models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, blank=True, null=True,default=None
    )
    @cached_property
    def file_field(self):
        return self.actual_file
