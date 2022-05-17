from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash, authenticate,
)
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class CustomLoginView(LoginView):

    authentication_form = AuthenticationForm


    template_name = 'auth/login.html'

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(self.request, username=username, password=password)
        if user and user.is_active:

            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "Veuillez vérifier vos coordonnées")
            return reverse_lazy('login')