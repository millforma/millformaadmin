import io
import zipfile
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.files.base import ContentFile
from main.models.file.document_type import DocumentType
from main.models.file.pdf_document import PdfDocument


def save_file_in_db(pdffile, formation_session, name, user, doc_type):
    file = ContentFile(pdffile, name=name)
    try:
        PdfDocument.objects.get(formation_session=formation_session, original_filename=name)
    except ObjectDoesNotExist:
        try:
            type = DocumentType.objects.get(name=doc_type)
        except DocumentType.DoesNotExist:
            type = DocumentType.objects.create(name=doc_type)
        temp = PdfDocument.objects.create(formation_session=formation_session, actual_file=file, original_filename=name,
                                          creator=user.person, type_of_document=type)
        temp.save()
    except MultipleObjectsReturned:
        print("Already created pdf for this formation")
    else:
        pass


def generate_zip(files):
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()
