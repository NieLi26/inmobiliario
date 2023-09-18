from django import forms
from .models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'address', 'rut', 'phone', 'email')