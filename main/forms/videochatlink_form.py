from django import forms

from main.models.formationsession import FormationSession
from main.models.videochat import VideoChat
from main.widget import DatePickerInput, TimePickerInput


class SessionForm(forms.ModelForm):
    class Meta:
        model = VideoChat
        fields = ('date_start', 'time_start', 'date_end', 'time_end')
        widgets = {
            'date_start': DatePickerInput(),
            'date_end': DatePickerInput(),
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(SessionForm, self).__init__(*args, **kwargs)
        user = self.user




