from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from main.forms.profile_form import ProfileForm


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "main/edit-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My profile"

        user = self.request.user


        context["profile_form"] = ProfileForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            }
        )


        return context

    def post(self, request, *args, **kwargs):
        _p = request.POST
        _r = request.FILES
        profile_form = ProfileForm(_p,)
        profile_form.is_valid()

        return self.form_valid(
         profile_form)

    @staticmethod
    def get_success_url():
        return reverse_lazy("profile_edit_view")

    def form_invalid(
            self, profile_form
    ):
        # Taken from Django source code:
        """ If the form is invalid, render the invalid form. """
        return self.render_to_response(
            self.get_context_data(
                profile_form=profile_form,
            )
        )

    def form_valid(
            self, profile_form
    ):
        user = self.request.user
        if profile_form.is_valid():
            user.username = profile_form.cleaned_data["username"]
            user.first_name = profile_form.cleaned_data["first_name"]
            user.last_name = profile_form.cleaned_data["last_name"]
            user.email = profile_form.clean_email()
            user.save()
        person = user.person.as_person_typed()


        messages.success(self.request, "Profile successfully updated")
        return HttpResponseRedirect(self.get_success_url())
