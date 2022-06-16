from django import forms

from main.models.formationsession import FormationSession


class FormationSessionForm(forms.ModelForm):
    class Meta:
        model = FormationSession
        fields = ('year','old_num_formation','commercial','name','trainee','num_present_trainee',
                  'foad','training_site','teacher_name','opco_name',
                  'date_autorised_start','date_autorised_end','date_start','date_end','training_duration','client_account')

    def __init__(self, *args, **kwargs):

        super(FormationSessionForm, self).__init__(*args, **kwargs)

        self.fields['year'].label = "Année"
        self.fields['old_num_formation'].label = "Numéro de dossier"
        self.fields['commercial'].label = "Commercial"
        self.fields['name'].label = "Nom"
        self.fields['trainee'].label = "Stagiaire(s)"
        self.fields['num_present_trainee'].label = "Nombre de stagiaires"
        self.fields['foad'].label = "Formation à distance"
        self.fields['training_site'].label = "Lieu de formation"
        self.fields['teacher_name'].label = "Nom du formateur"
        self.fields['opco_name'].label = "Nom OPCO"
        self.fields['date_autorised_start'].label = "Date autorisée de début"
        self.fields['date_autorised_end'].label = "Date autorisée de fin"
        self.fields['date_start'].label = "Date de début"
        self.fields['date_end'].label = "Date de fin"
        self.fields['training_duration'].label = "Durée de la formation"
        self.fields['client_account'].label = "Client"


