import datetime
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


# get formation session from cirrushield
from cirrushieldapi.apiCalls import GetFormationSession
from cirrushieldapi.views.email_view import send_id
from main.models.formationsession import FormationSession


class SearchFormation(TemplateView, UserPassesTestMixin):
    template_name = 'main/importcirrus.html'

    def test_func(self):
        return self.request.user.groups.filter(name='commercial').exists()

    def post(self, request):
        num_doss = request.POST.get("num_dossier")

        formation_session = GetFormationSession(num_doss)
        try:
            FormationSession.objects.get(old_num_formation=num_doss)

        except FormationSession.DoesNotExist:


            list_of_tuples = FormationSession.OPCO_NAMES_CHOICES

            # ✅ get list of all indices of tuples that match the condition

            result = [
                idx for idx, tup in enumerate(list_of_tuples) if tup[1] == formation_session['Data']['Contrat_de_Formation']['OPCO']
            ]

            final_session = FormationSession.objects.create(year=formation_session['Data']['Contrat_de_Formation']['Annee_du_contrat'],
                                                            old_num_formation=num_doss,
                                                            commercial=formation_session['Data']['Contrat_de_Formation']['Commercial_principal'],
                                                            client_account=formation_session['Data']['Contrat_de_Formation']['Client_Account'],
                                                            name=formation_session['Data']['Contrat_de_Formation']['Name'],
                                                            num_present_trainee=formation_session['Data']['Contrat_de_Formation']['Number_of_Trainees'],
                                                            foad=True if (formation_session['Data']['Contrat_de_Formation']['Formation_a_distance_liste']=='Oui') else False,
                                                            training_site=formation_session['Data']['Contrat_de_Formation']['Numero_de_la_rue'],
                                                            teacher_name=formation_session['Data']['Contrat_de_Formation']['Formateur'],
                                                            opco_name=result[0],
                                                            date_autorised_start=((datetime.datetime.strptime(formation_session['Data']['Contrat_de_Formation']['Authorized_Start_Date'], '%Y-%m-%d')) + datetime.timedelta(
                                                                days=1)) if formation_session['Data']['Contrat_de_Formation']['Authorized_Start_Date'] else (
                                                            formation_session['Data']['Contrat_de_Formation']['Authorized_Start_Date']),
                                                            date_autorised_end=((datetime.datetime.strptime(formation_session['Data']['Contrat_de_Formation']['Authorized_End_Date'], '%Y-%m-%d')) + datetime.timedelta(
                                                                days=1)) if formation_session['Data']['Contrat_de_Formation']['Authorized_End_Date'] else (
                                                            formation_session['Data']['Contrat_de_Formation']['Authorized_End_Date']),
                                                            date_start=((datetime.datetime.strptime(formation_session['Data']['Contrat_de_Formation']['Expected_Start_Date'], '%Y-%m-%d')) + datetime.timedelta(
                                                                days=1)) if formation_session['Data']['Contrat_de_Formation']['Expected_Start_Date'] else (
                                                            formation_session['Data']['Contrat_de_Formation']['Expected_Start_Date']),
                                                            date_end=((datetime.datetime.strptime(formation_session['Data']['Contrat_de_Formation']['Expected_End_Date'], '%Y-%m-%d')) + datetime.timedelta(days=1)) if
                                                            formation_session['Data']['Contrat_de_Formation']['Expected_End_Date'] else (
                                                            formation_session['Data']['Contrat_de_Formation']['Expected_End_Date']),
                                                            training_duration=int(formation_session['Data']['Contrat_de_Formation']['Total_Number_of_Training_Hours']),
                                                            teacher_price=int(formation_session['Data']['Contrat_de_Formation']['Cout_du_formateur']),
                                                            )

            final_session.objectifs_peda.set(formation_session['Data']['Contrat_de_Formation']['Training_Offer'])

            final_session.trainee.set(formation_session['Data']['Contrat_de_Formation']['Stagiaires'])
            final_session.save()

            current_site = Site.objects.get_current()
            link_reset_passwd = 'https://www.millforma-admin.fr' + '/password-reset/'
            #send_id(link_reset_passwd, final_session, current_site)
            messages.success(self.request, "La session a bien été importée")

        return redirect('main:home')
