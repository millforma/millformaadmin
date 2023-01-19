from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from main.models.file.document_type import DocumentType
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession


class AttendanceSignListView(LoginRequiredMixin, ListView):
    template_name = 'pdf/attendance_sign_list.html'
    model = PdfDocument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formation_session = self.kwargs['formation_id']
        formation_session = FormationSession.objects.get(id=formation_session)
        type = DocumentType.objects.filter(name__in=[1, 9])

        pdf_files = PdfDocument.objects.filter(formation_session=formation_session, type_of_document__in=type).exclude(
            is_signed_by=self.request.user)

        context['files'] = pdf_files
        context['formation_session'] = formation_session

        return context