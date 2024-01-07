import datetime
import json
from django.contrib.sites.models import Site
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import resolve_url
from django.views.generic import FormView
from django.contrib import messages
from cirrushieldapi.apiCalls import GetFormationSession
from cirrushieldapi.forms.formation_session_form import FormationSessionForm
from cirrushieldapi.views.email_view import send_id
from main.models.formationsession import FormationSession, Objectifs_peda


# Create Formation session on sumbit of formation_session_form
class SaveFormation(FormView, UserPassesTestMixin):
    template_name = 'main/formation-session-save.html'
    form_class = FormationSessionForm

    def test_func(self):
        return self.request.user.groups.filter(name='commercial').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formation_id = self.kwargs["formation_id"]
        formation_session = GetFormationSession(formation_id)

        context["form"] = FormationSessionForm(
            initial={
                "year": formation_session['Data']['Contrat_de_Formation']['Annee_du_contrat'],
                "commercial": formation_session['Data']['Contrat_de_Formation']['Commercial_principal'],
                "client_account": formation_session['Data']['Contrat_de_Formation']['Client_Account'],
                "name": formation_session['Data']['Contrat_de_Formation']['Name'],
                "trainee": formation_session['Data']['Contrat_de_Formation']['Stagiaires'],
                "num_present_trainee": formation_session['Data']['Contrat_de_Formation']['Number_of_Trainees'],
                "foad": formation_session['Data']['Contrat_de_Formation']['Formation_a_distance_liste'],
                "training_site": formation_session['Data']['Contrat_de_Formation']['Numero_de_la_rue'],
                "teacher_name": formation_session['Data']['Contrat_de_Formation']['Formateur'],
                "opco_name": formation_session['Data']['Contrat_de_Formation']['OPCO'],
                "date_autorised_start": formation_session['Data']['Contrat_de_Formation']['Authorized_Start_Date'],
                "date_autorised_end": formation_session['Data']['Contrat_de_Formation']['Authorized_End_Date'],
                "date_start": formation_session['Data']['Contrat_de_Formation']['Expected_Start_Date'],
                "date_end": formation_session['Data']['Contrat_de_Formation']['Expected_End_Date'],
                "training_duration": int(
                    formation_session['Data']['Contrat_de_Formation']['Total_Number_of_Training_Hours']),
                "teacher_price": formation_session['Data']['Contrat_de_Formation']['Cout_du_formateur'],
                "objectifs_peda":formation_session['Data']['Contrat_de_Formation']['Training_Offer'],
                "old_num_formation": formation_id,

            }
        )
        return context

    def get_success_url(self):
        return resolve_url('main:home')

    def form_valid(self, form):
        if form.is_valid():
            try:
                FormationSession.objects.get(old_num_formation=form.cleaned_data["old_num_formation"])
            except FormationSession.DoesNotExist:

                final_session = FormationSession.objects.create(year=form.cleaned_data["year"],
                                                                old_num_formation=form.cleaned_data[
                                                                    "old_num_formation"],
                                                                commercial=form.cleaned_data["commercial"],
                                                                client_account=form.cleaned_data["client_account"],
                                                                name=form.cleaned_data["name"],
                                                                num_present_trainee=form.cleaned_data[
                                                                    "num_present_trainee"],
                                                                foad=form.cleaned_data["foad"],
                                                                training_site=form.cleaned_data["training_site"],
                                                                teacher_name=form.cleaned_data["teacher_name"],
                                                                opco_name=form.cleaned_data["opco_name"],
                                                                date_autorised_start=(form.cleaned_data[
                                                                    "date_autorised_start"]+datetime.timedelta(days=1)) if form.cleaned_data["date_autorised_start"] else (form.cleaned_data["date_autorised_start"]),
                                                                date_autorised_end=(form.cleaned_data[
                                                                    "date_autorised_end"]+datetime.timedelta(days=1)) if form.cleaned_data["date_autorised_end"] else (form.cleaned_data["date_autorised_end"]),
                                                                date_start=(form.cleaned_data["date_start"]+datetime.timedelta(days=1)) if form.cleaned_data["date_start"] else (form.cleaned_data["date_start"]),
                                                                date_end=(form.cleaned_data["date_end"]+datetime.timedelta(days=1)) if form.cleaned_data["date_end"] else (form.cleaned_data["date_end"]),
                                                                training_duration=form.cleaned_data[
                                                                    "training_duration"],
                                                                teacher_price=form.cleaned_data["teacher_price"],
                                                                )

                final_session.objectifs_peda.set(form.cleaned_data["objectifs_peda"])

                final_session.trainee.set(form.cleaned_data["trainee"])
                final_session.save()
                current_site = Site.objects.get_current()
                link_reset_passwd = 'https://www.millforma-admin.fr' + '/password-reset/'
                #send_id(link_reset_passwd, final_session, current_site)
                messages.success(self.request, "La session a bien été importée")

        return super(SaveFormation, self).form_valid(form)
