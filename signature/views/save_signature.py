from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
from jsignature.utils import draw_signature
from signature.decorators import send_verification_code
from signature.forms import SignatureForm
from signature.models import SignatureModel

class SaveSignatureView(LoginRequiredMixin, TemplateView):
    template_name = 'pdf/save_signature.html'

    def dispatch(self, request, *args, **kwargs):
        request.user=self.request.user
        return super(SaveSignatureView, self).dispatch(request, *args, **kwargs)

    @send_verification_code
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignatureForm()
        messages.success(self.request, "Veuillez vérifier votre email pour le code de vérification")
        return context

    def post(self, request, *args, **kwargs):
        _p = request.POST
        signature_form = SignatureForm(_p)
        signature_form.is_valid()
        return self.form_valid(signature_form)

    @staticmethod
    def get_success_url():
        return reverse('main:home')

    def form_invalid(self, signature_form):
        # Taken from Django source code:
        """ If the form is invalid, render the invalid form. """

        return self.render_to_response(
            self.get_context_data(
                signature_form=signature_form
            )
        )

    def form_valid(self, signature_form):
        user = self.request.user
        if signature_form.is_valid():
            signature = signature_form.cleaned_data.get('signature')
            if signature:
                signature_file_path = draw_signature(signature, as_file=True)

                if signature_form.cleaned_data['verification_code'] == user.person.user_verification_code:
                    result = SignatureModel.objects.create(signature_owner=user, signature=signature_file_path)
                    result.save()
                    messages.success(self.request, _("Merci, votre signature est désormais enregistrée !"))
                else:
                    messages.error(self.request, _("Le code de vérification est erroné. Veuillez vérifier votre boite mail"))
                    return self.form_invalid(signature_form)

        return redirect(self.get_success_url())
