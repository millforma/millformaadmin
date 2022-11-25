from django import forms
from main.models.videochat import VideoChat
from main.widget import DatePickerInput, TimePickerInput


class SessionForm(forms.ModelForm):
    class Meta:
        model = VideoChat
        fields = ('date_start', 'time_start', 'time_end')
        widgets = {
            'date_start': DatePickerInput(),
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['date_start'].label = "Date du jour"
        self.fields['time_start'].label = "Heure de début"
        self.fields['time_end'].label = "Heure de fin"




