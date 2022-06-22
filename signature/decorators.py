from functools import wraps
import random

from cirrushieldapi.views.email_view import send_email_verification_code
from main.models.file.pdf_document import PdfDocument



def send_verification_code(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            doc_id = kwargs['doc_id']
            doc = PdfDocument.objects.get(id=doc_id)

            code = random.randint(1111, 9999)

            send_email_verification_code(request.request, code)

            doc.verification_code = code
            doc.save()
            return function(request, *args, **kwargs)

        except KeyError:
            return function(request, *args, **kwargs)

    return wrap
