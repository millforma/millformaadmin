from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from main.models.formationsession import FormationSession


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "main/index.html"

    def test_func(self):
        return self.request.user.groups.filter(name__in=['commercial','teacher']).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='teacher').exists():

            if self.request.GET.get('all_formations'):
                UserFormationSessions = FormationSession.objects.filter(teacher_name=self.request.user)
            elif self.request.GET.get('to_be_organised'):
                UserFormationSessions = FormationSession.objects.filter(completed_videochat_sessions=0,teacher_name__contains=self.request.user)
            elif self.request.GET.get('finished'):
                UserFormationSessions = FormationSession.objects.filter(is_finished=True,teacher_name__contains=self.request.user)
            elif self.request.GET.get('in_progress'):
                UserFormationSessions = FormationSession.objects.filter(date_start__isnull=False, is_finished=False,teacher_name__contains=self.request.user)
            else:
                UserFormationSessions = FormationSession.objects.filter(teacher_name=self.request.user)
            context['group'] = 'teacher'
        else:

            if self.request.GET.get('all_formations'):
                UserFormationSessions = FormationSession.objects.all()
            elif self.request.GET.get('to_be_organised'):
                UserFormationSessions = FormationSession.objects.filter(completed_videochat_sessions=0)
            elif self.request.GET.get('finished'):
                UserFormationSessions = FormationSession.objects.filter(is_finished=True)
            elif self.request.GET.get('in_progress'):
                UserFormationSessions = FormationSession.objects.filter(date_start__isnull=False, is_finished=False)
            else:
                UserFormationSessions = FormationSession.objects.all()
            context['group'] = 'commercial'

        context['formation_list'] = UserFormationSessions


        return context
