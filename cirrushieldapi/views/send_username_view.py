from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.views.generic import FormView

from cirrushieldapi.forms.username_form import UsernameForm
from cirrushieldapi.views.email_view import resend_username


class SendUsername(FormView):
    template_name = 'registration/username_send_form.html'
    form_class = UsernameForm


    def get_success_url(self):
        return resolve_url('cirrushieldapi:username_send')

    def form_valid(self, form):
        if form.is_valid():
            try:

                user=User.objects.get(email=form.cleaned_data['email'])
                resend_username(user)
            except User.DoesNotExist:

                messages.error(self.request, "L'adresse email n'est associée à aucun compte")

        return super(SendUsername, self).form_valid(form)
