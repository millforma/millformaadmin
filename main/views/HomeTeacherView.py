from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from cirrushieldapi.views.email_view import send_emargement_trainees
from main.forms.videochatlink_form import SessionForm
from main.models import Event
from main.models.formationsession import FormationSession
from main.models.videochat import VideoChat
from main.views.emargement_view import Generate_emargement


class CreateVideoChatView(LoginRequiredMixin,UserPassesTestMixin, FormView):
    template_name = "session/create_session.html"
    form_class = SessionForm

    def test_func(self):
        return self.request.user.groups.filter(name='teacher').exists()

    def get_form_kwargs(self):
        kwargs = super(CreateVideoChatView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('main:session', kwargs={'formation_id': self.kwargs['formation_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formation_session_id = self.kwargs["formation_id"]
        formation_session = FormationSession.objects.get(id=formation_session_id)
        context["formation_session"] = formation_session
        return context

    def form_valid(self, form):
        if form.is_valid():
            formation_session_id = self.kwargs["formation_id"]
            formation = FormationSession.objects.get(id=formation_session_id)
            if form.is_valid():

                video_chat_date_start = form.cleaned_data["date_start"]
                video_chat_time_start = form.cleaned_data["time_start"]

                start = datetime(video_chat_date_start.year, video_chat_date_start.month, video_chat_date_start.day,
                                 video_chat_time_start.hour, video_chat_time_start.minute,
                                 video_chat_time_start.second)


                video_chat_end_time = form.cleaned_data["time_end"]

                end = datetime(video_chat_date_start.year, video_chat_date_start.month, video_chat_date_start.day,
                               video_chat_end_time.hour, video_chat_end_time.minute,
                               video_chat_end_time.second)

                timedelta = end - start
                if timedelta.seconds % 3600 == 0:

                    try:

                        video_chat = VideoChat.objects.create(
                            created_by=self.request.user,
                            formation_session=formation,
                            title="Video Chat N° " + str(
                                formation.completed_videochat_sessions + 1) + " For: " + str(
                                formation.name),
                            session=formation.completed_videochat_sessions + 1,
                            date_start=form.cleaned_data["date_start"],
                            time_start=form.cleaned_data["time_start"],
                            date_end=form.cleaned_data["date_start"],
                            time_end=form.cleaned_data["time_end"],
                            finished_session=True)

                        start = datetime(video_chat.date_start.year, video_chat.date_start.month,
                                         video_chat.date_start.day,
                                         video_chat.time_start.hour, video_chat.time_start.minute,
                                         video_chat.time_start.second)
                        date_start_event = start.strftime("%Y-%m-%dT%H:%M:%S")

                        formation = video_chat.formation_session
                        formation.completed_videochat_sessions += 1
                        formation.date_start = video_chat_date_start
                        formation.save()

                        end = datetime(video_chat.date_end.year, video_chat.date_end.month, video_chat.date_end.day,
                                       video_chat.time_end.hour, video_chat.time_end.minute,
                                       video_chat.time_end.second)
                        date_end_event = end.strftime("%Y-%m-%dT%H:%M:%S")

                        event = Event.objects.create(user=self.request.user,
                                                     teacher=formation.teacher_name,
                                                     formation_session=formation,
                                                     title="Video Chat N° " + str(
                                                         formation.completed_videochat_sessions + 1) + " For: " + str(
                                                         formation.name),
                                                     start_time=date_start_event,
                                                     end_time=date_end_event,
                                                     video_chat=video_chat)
                        delta = end - start
                        period = delta.total_seconds() / 3600 + formation.training_done
                        formation.training_done = period
                        formation.save()
                        if formation.training_done >= formation.training_duration:
                            formation.is_finished = True

                            formation.save()
                        Generate_emargement(request=self.request, formation_id=formation.id, event=event.id)
                        send_emargement_trainees(self.request,formation.id,date_start_event)
                        messages.add_message(self.request, messages.SUCCESS,
                                             'La session est crée, la demande de signature a été envoyée aux stagiaires')

                    except IntegrityError:
                        messages.add_message(self.request, messages.ERROR,
                                             'Erreur une session porte déjà cet ID')
                else:
                    messages.add_message(self.request, messages.ERROR, 'Veuillez utiliser des heures pleines uniquement')

        return super(CreateVideoChatView, self).form_valid(form)


class ListVideoChatView(LoginRequiredMixin, TemplateView):
    template_name = "session/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formation_session = FormationSession.objects.get(id=self.kwargs['formation_id'])
        context['videoChatList'] = VideoChat.objects.filter(formation_session_id=formation_session.id)
        context['formation_session'] = formation_session
        return context


