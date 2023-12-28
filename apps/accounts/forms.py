from django.contrib.auth.models import Group
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    AuthenticationForm
)
from .models import Agent, AgentProfile, Admin
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from .rut_chile import is_valid_rut

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


User = get_user_model()

non_allowed_usernames = ['abc']


# Every letter to UpperCase(charfield)
class UpperCase(forms.CharField):
    def to_python(self, value):
        return value.upper()


attrs_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
attrs_class_error = 'focus:outline-none border border-red-500 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'


# por defecto el usuario normal de django solo me pide el username y password para poder crearme un cuenta
# si lo dejara asi nada mas, me pediria usar el modelo por defecto en 'from django.contrib.auth.models import User'
# pero como hice un usuario personalizado y lo asigne como usuario por defecto, debo sobrescribir el usuario por defecto en el 'class Meta'
# class CustomUserCreationForm(UserCreationForm): 
#     pass
# class CustomUserChangeForm(UserChangeForm):
#     pass

############################################################################################################################################
######################################################## FORMULARIOS POR DEFECTO SOBRESCRITOS ##############################################
############################################################################################################################################
class CustomUserCreationForm(UserCreationForm): # campo de contraseña se incluye implicitamente cuando heredamos este formulario

    email = forms.EmailField(
        required=True, label='Dirección de correo electrónico')
    rut = UpperCase(required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    terms = forms.BooleanField(required=True, label='Declaro conocer y aceptar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'terms':
                self.fields[field].widget.attrs['class'] = attrs_class
                if self.errors.get(field):
                    self.fields[field].widget.attrs['class'] = attrs_class_error
            else:
                self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                if self.errors.get(field):
                    self.fields[field].widget.attrs['class'] = 'focus:outline-none border border-red-500 h-4 w-4 rounded appearance-none leading-normal text-gray-700'

        data = {
            'x-mask': '99.999.999-*',
            'placeholder': 'Ej. 99999999-9',
        }
        self.fields['rut'].widget.attrs.update(data)
        # self.fields['rut'].widget.attrs['class'] += ' uppercase' 
      
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'rut', 'phone', 'email', 'username', 'password1', 'password2', 'captcha', 'terms')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        msg = ["El rut es invalido", "Ingrese sin puntos y con guion"]
        if not is_valid_rut(rut):
            raise forms.ValidationError(msg)
        # try:
         
        # except:
        #     raise forms.ValidationError(msg)
        return rut


class CustomUserChangeForm(UserChangeForm): # campo de contraseña se incluye implicitamente cuando heredamos este formulario
    class Meta:
        model = User
        fields = ('email', 'username')


class CustomUserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


############################################################################################################################################
######################################################## FORMULARIOS PERSONALIZADOS ########################################################
############################################################################################################################################
class CustomLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'ingrese su nombre de usuario'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'ingrese su contraseña'}))
   
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            msg = 'Este nombre de usuario no es valido'
            raise forms.ValidationError(msg)
        return username


################ registro 1 sin modelo ##################
class CustomRegisterForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'ingrese su nombre de usuario'}))
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'ingrese su contraseña'}))
    password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'ingrese nuevamente su contraseña'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if username in non_allowed_usernames:
            msg = 'Este nombre de usuario no es valido, escoja otro'
            raise forms.ValidationError(msg)
        if qs.exists():
            msg = 'Este nombre de usuario no es valido, escoja otro'
            raise forms.ValidationError(msg)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            msg = 'Este correo ya esta en uso'
            raise forms.ValidationError(msg)
        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            msg = "Las contrasenas no son iguales"
            self.add_error('password2', msg)
        return cleaned_data

    # opcion para crearlo aqui al usuario
    # def save(self, commit=True):
    #     user = User.objects.create_user(
    #         self.cleaned_data["username"],
    #         self.cleaned_data["email"],
    #         self.cleaned_data["password1"],
    #     )
    #     return user


################# registro 2 con modelo #################
class UserRegistrationForm(forms.ModelForm):

    """
    en este caso como estamos usando un forms.modelForm se usa el metodo set_password en el metodo save, 
    y en el caso de yo llamar directamente al modelo user en una lista o usar un formulario forms.Form 
    es conveniente que se cree el usuario de la siguiente forma `User.objectes.create_user()`? 
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']
        
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


###################### AGENTE FORM #######################|
class AgentCreationForm(UserCreationForm):

    start_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Inicio Contrato'
    )

    end_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Termino Contrato'
    )

    zone = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Zona'
    )

    class Meta:
        model = Agent
        # solo incluye username, password 1 y password 2
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone', 'rut')

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut = rut.lower()
        if User.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            msg = 'El rut ya se encuentra en uso'
            raise forms.ValidationError(msg)
        if not is_valid_rut(rut):
            msg = ["El rut es invalido", "Ingrese sin puntos y con guion"]
            raise forms.ValidationError(msg)
        return rut
    
    def clean(self):
        clean_data = super().clean()
        start_contract = clean_data.get('start_contract')
        end_contract = clean_data.get('end_contract')
        # ==== evitar hora de inicio mayor que la de termino, o igual
        if start_contract and end_contract:
            if start_contract > end_contract:
                msg = 'La fecha de inicio de contrato no puede ser mayor a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
            if start_contract == end_contract:
                msg = 'La fecha  de inicio de contrato no puede ser igual a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
        return clean_data
    
        
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         if user.tipo == "AGE":
    #             group, _ = Group.objects.get_or_create(name='Agente')
    #             user.groups.add(group)
    #         elif user.tipo == "ADM":
    #             group, _ = Group.objects.get_or_create(name='Administrador')
    #             user.groups.add(group)
    #     return user


class AgentChangeForm(UserChangeForm):

    password = None

    start_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Inicio Contrato'
    )

    end_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Termino Contrato',
    )

    zone = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Zona'
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        valores_iniciales = {
            'start_contract': self.instance.agentprofile.start_contract.strftime('%Y-%m-%d') if self.instance.agentprofile else '',
            'end_contract': self.instance.agentprofile.end_contract.strftime('%Y-%m-%d') if self.instance.agentprofile else '', 
            'zone': self.instance.agentprofile.zone if self.instance.agentprofile else ''
        }

        for key, value in valores_iniciales.items():
            self.fields[key].initial = value
               
    class Meta:
        model = Agent
        # solo incluye username, password 1 y password 2
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'rut')

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut = rut.lower()
        if User.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            msg = 'El rut ya se encuentra en uso'
            raise forms.ValidationError(msg)
        if not is_valid_rut(rut):
            msg = ["El rut es invalido", "Ingrese sin puntos y con guion"]
            raise forms.ValidationError(msg)
        return rut
    
    def clean(self):
        clean_data = super().clean()
        start_contract = clean_data.get('start_contract')
        end_contract = clean_data.get('end_contract')
        # ==== evitar hora de inicio mayor que la de termino, o igual
        if start_contract and end_contract:
            if start_contract > end_contract:
                msg = 'La fecha de inicio de contrato no puede ser mayor a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
            if start_contract == end_contract:
                msg = 'La fecha  de inicio de contrato no puede ser igual a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
        return clean_data
    

class AgentProfileForm(forms.ModelForm):

    zone = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Zona'
    )

    start_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Inicio Contrato'
    )

    end_contract = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Termino Contrato'
    )

    class Meta:
        model = AgentProfile
        fields = ('start_contract', 'end_contract', 'zone')

    def clean(self):
        clean_data = super().clean()
        start_contract = clean_data.get('start_contract')
        end_contract = clean_data.get('end_contract')
        # ==== evitar hora de inicio mayor que la de termino, o igual
        if start_contract and end_contract:
            if start_contract > end_contract:
                msg = 'La fecha de inicio de contrato no puede ser mayor a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
            if start_contract == end_contract:
                msg = 'La fecha  de inicio de contrato no puede ser igual a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
        return clean_data
    

###################### ADMIN FORM #######################|
class AdminCreationForm(UserCreationForm):

    class Meta:
        model = Admin
        # solo incluye username, password 1 y password 2
        # fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone', 'rut')
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone', 'rut')

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut = rut.lower()
        if User.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            msg = 'El rut ya se encuentra en uso'
            raise forms.ValidationError(msg)
        if not is_valid_rut(rut):
            msg = ["El rut es invalido", "Ingrese sin puntos y con guion"]
            raise forms.ValidationError(msg)
        return rut
    
    def clean(self):
        clean_data = super().clean()
        start_contract = clean_data.get('start_contract')
        end_contract = clean_data.get('end_contract')
        # ==== evitar hora de inicio mayor que la de termino, o igual
        if start_contract and end_contract:
            if start_contract > end_contract:
                msg = 'La fecha de inicio de contrato no puede ser mayor a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
            if start_contract == end_contract:
                msg = 'La fecha  de inicio de contrato no puede ser igual a la fecha de termino de contrato'
                self.add_error('start_contract', msg)
        return clean_data
    