from django.contrib import admin

# Register your models here.
from main.models.file.pdf_document import PdfDocument

admin.site.register(PdfDocument)