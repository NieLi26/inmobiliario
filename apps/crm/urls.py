from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path(
        route='clients/',
        view=views.ClientListCreateView.as_view(),
        name='client_list'
    )
]

hx_patterns = [
    path(
        route='clients/table',
        view=views.TableClientView.as_view(),
        name='client_table'
    ),
    path(
        route='clients/<int:pk>/',
        view=views.ClientRetrieveUpdateDestroyView.as_view(),
        name='client_detail'
    ),
]

urlpatterns += hx_patterns
