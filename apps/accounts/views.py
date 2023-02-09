from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model

#cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import (CustomUserCreationForm, CustomLoginForm,
                    CustomRegisterForm, CustomUserLoginForm)

User = get_user_model()


# Custom
def register_view(request):
    form = CustomRegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        # para evitar algun error con la creacion
        try:
            user = User.objects.create_user(username, email, password=password) # se crear y se autentica solo
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect("/")
        else:
            request.session['register_error'] = 1 # 1==True
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    form = CustomLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password) # si es valido retorna una instancia de un usuario
        if user != None:
            # user is valid and active
            # request.user == user
            login(request, user)
            return redirect("/")
        else:
            # attempt = request.session.get('attempt') or 0
            # request.session['attempt'] = attempt + 1
            request.session['invalid_user'] = 1 # 1==True
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    #request.user == Anonymous User
    logout(request)
    return redirect('/')

# Overriding
@method_decorator(never_cache, name='dispatch')
class SignupPageView(CreateView): # no me loguea enseguida, solo crea la cuenta
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LoginPageView(LoginView): 
    authentication_form = CustomUserLoginForm  # es mejor usar estar forma en ves de form_class, pq este atributo se usa para indicar si se usara un formulario personalizado, form_class ya apunta al formulario por defecto
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginPageView, self).dispatch(request, *args, **kwargs)
    