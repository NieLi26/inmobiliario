from django import forms
from django.core.validators import RegexValidator


# Every letter to LowerCase(charfield)
class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()


# Every letter to UpperCase(charfield)
class UpperCase(forms.CharField):
    def to_python(self, value):
        return value.upper()


# Every letter to Capitalize(charfield)
class Capitalize(forms.CharField):
    def to_python(self, value):
        return value.capitalize()


number_validator = RegexValidator(
    regex=r'^[1-9]\d*$',
    message=[
        'Este campo solo debe contener números.',
        'Debe ser mayor a 0.'
    ]
)


email_validator = RegexValidator(
    regex=r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$',
    message=[
        'Introduzca una dirección de correo electrónico válida.',
    ]
)

number_decimal_validator = RegexValidator(
    regex=r'^([1-9]\d*(\.\d+)?|0\.\d+)$',
    message=[
        'Este campo solo debe contener números.',
        'Debe ser mayor a 0.'
    ]
)

attrs_class = 'focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'
attrs_class_error = 'focus:outline-none border border-red-500 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'
