from django import forms
from . models import NewsletterUser

class NewsletterUserForm(forms.ModelForm):

    # email = forms.EmailField(error_messages={'required': 'Ingresa un correo electrónico',  'invalid': 'El correo electrónico ingresado no es válido'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = "block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform bg-transparent border border-transparent rounded-md focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"
        self.fields['email'].widget.attrs['placeholder'] = "Ingreso su correo"
        # self.fields['email'].error_messages['invalid'] = 'Este campo es requerido.'
    class Meta:
        model = NewsletterUser
        fields = ('email',)
