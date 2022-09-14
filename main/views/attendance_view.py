from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession


class AttendanceView(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    template_name = "main/viewattendance.html"

    def test_func(self):
        return self.request.user.groups.filter(name='commercial').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formation_id = self.kwargs['formation_id']
        formation = FormationSession.objects.get(id=formation_id)
        trainees = formation.trainee.all()
        docs = PdfDocument.objects.filter(formation_session=formation, type_of_document=1)

        context['formation'] = formation
        context['trainees'] = trainees
        context['docs'] = docs

        return context
