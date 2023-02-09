import re
from django.forms import TextInput
from django.urls import reverse_lazy
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Contact, OwnerContact

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'
        # self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('home')
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_method = 'post'
        # self.helper.form_class = 'blueForms'
        
        # self.helper.add_input(Submit('submit', 'Submit'))
 
    class Meta:
        model = Contact
        exclude = ('state', )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '' :
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone
class OwnerContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'
    class Meta:
        model = OwnerContact
        exclude = ('state',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '' :
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone