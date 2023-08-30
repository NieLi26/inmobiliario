from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    # CONTACT LIST
    path('contact/', views.ContactListView.as_view(), name='contact_list'),
    path('contact/create/', views.ContactPageView.as_view(), name='contact_create'),
    
    path('test/', views.TestTemplateView.as_view(), name='test')

    # ELIMINADO
    # CONTACT OWNER LIST
    # path('contact-owner/', views.OwnerContactListView.as_view(), name='contact_owner_list'),
]


hxpatterns = [
    # CONTACT FORM
    path('subject-select', views.hx_subject_select, name='subject_select'),
    # CONTACT LIST
    path('hx_contact_table/<int:page_number>/', views.hx_contact_table, name='hx_contact_table'),
    path('hx_contact_modal/<int:pk>/<int:page_number>/', views.hx_contact_modal, name='hx_contact_modal'),
    path('hx_contact_notify/', views.hx_contact_notify, name='hx_contact_notify'),
    # HOME LIST
    path('hx_search_location/', views.hx_search_location, name='hx_search_location'),
    path('hx_contact_home_form/', views.hx_contact_home_form, name='hx_contact_home_form'),
    path('hx_side_alert/', views.hx_side_alert, name='hx_side_alert'),
    # path('hx_message/', hx_message, name='hx_message'),

    # ELIMINADO
    # CONTACT OWNER LIST
    # path('hx_contact_owner_table/<int:page_number>/', views.TableOwnerContactView.as_view(), name='hx_contact_owner_table'),
    # path('hx_contact_owner_modal/<int:pk>/<int:page_number>/', views.ModalOwnerContactView.as_view(), name='hx_contact_owner_modal'),
]

urlpatterns += hxpatterns