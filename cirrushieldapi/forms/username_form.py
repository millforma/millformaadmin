from django import forms

class UsernameForm(forms.Form):
    email=forms.EmailField(label='Renseignez votre email',max_length=100)