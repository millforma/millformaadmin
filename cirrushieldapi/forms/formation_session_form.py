from django import forms

from main.models.formationsession import FormationSession


class FormationSessionForm(forms.ModelForm):
    class Meta:
        model = FormationSession
        fields = ('year','old_num_formation','commercial','name','trainee','num_present_trainee',
                  'foad','training_site','teacher_name','opco_name',
                  'date_autorised_start','date_autorised_end','date_start','date_end','training_duration','client_account')
