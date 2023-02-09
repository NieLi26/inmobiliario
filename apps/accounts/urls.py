from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignupPageView, login_view, logout_view, register_view, LoginPageView

app_name = 'accounts'

urlpatterns = [
    ## Opcion 1, habilitada 
    # creada para usarse con la autenticacion que te provee django
    path("signup/", SignupPageView.as_view(), name="signup") ,

    # creado para remplazar el por defecto y pasarle el recaptcha
    path("login/", LoginPageView.as_view(), name="login") ,

    ## Opcion 2, no habilitada
    # creadas para usuarlos personalizadamente
    # path("login-view/", login_view, name="login_view") ,
    # path("logout-view/", logout_view, name="logout_view") ,
    # path("register-view/", register_view, name="register_view") ,

]