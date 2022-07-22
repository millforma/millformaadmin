from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _



class MySetPasswordForm(SetPasswordForm):
    error_messages = {'password_mismatch': _('Les deux mots de passe ne correspondent pas.'), }

    new_password1 = forms.CharField(label=_("Nouveau mot de passe"),
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), strip=False,
                                    help_text="Votre mot de passe doit contenir au moins 8 caractères dont 1 chiffre", )

    new_password2 = forms.CharField(label=_("Confirmation du nouveau mot de passe"), strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), )