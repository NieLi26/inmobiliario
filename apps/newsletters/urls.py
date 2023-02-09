from django.urls import path

from . import views

app_name = 'newsletters'

urlpatterns = [
    path('create/', views.NewsletterUserView.as_view(), name='create')
]