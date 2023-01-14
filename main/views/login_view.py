from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
     login as auth_login, authenticate,
)
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class CustomLoginView(LoginView):

    authentication_form = AuthenticationForm


    template_name = 'auth/login.html'

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(self.request, username=username, password=password)
        if user and user.is_active:
            if user.last_login is None:
                auth_login(self.request, form.get_user())
                return redirect('signature:save_signature')
            else:
                return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "Veuillez vérifier vos coordonnées")
            return reverse_lazy('login')