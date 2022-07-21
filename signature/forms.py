"""
    Provides a django form field to handle a signature capture field with
    with jSignature jQuery plugin
"""
import json
from django.forms.fields import Field
from django.core import validators
from django.core.exceptions import ValidationError
from .widgets import JSignatureWidget
from django import forms

JSIGNATURE_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )


class JSignatureField(Field):
    """
    A field handling a signature capture field with with jSignature
    """
    widget = JSignatureWidget()

    def to_python(self, value):
            """
            Validates that the input can be red as a JSON object.
            Returns a Python list (JSON object unserialized).
            """
            if value in JSIGNATURE_EMPTY_VALUES:
                return None
            try:
                return json.loads(value)
            except ValueError:
                raise ValidationError('Invalid JSON format.')





class SignatureForm(forms.Form):
    signature = JSignatureField()
    verification_code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(SignatureForm, self).__init__(*args, **kwargs)

        self.fields['signature'].label = "Merci de signer dans le cadre ci-dessous"
        self.fields['verification_code'].label = "Code de vérification envoyé par e-mail"

