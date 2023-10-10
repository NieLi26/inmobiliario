from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    # Test
    path('<str:property_type>/create/test/', views.property_create_test, name='property_create_test'),
    
    ## PANEL
    # path('panel/publicaciones/', views.property_publish_list, name='property_custom_publish'), 
    # path('panel/despublicaciones/', views.DraftListView.as_view(), name='property_custom_draft'), 

    path('panel/publicaciones/venta/', views.PublishBuyListView.as_view(), name='publish_buy_list'),
    path('panel/publicaciones/permuta/', views.PublishExchangeListView.as_view(), name='publish_exchange_list'),
    path('panel/publicaciones/arriendo/', views.PublishRentListView.as_view(), name='publish_rent_list'),
    path('panel/publicaciones/arriendo-temporada/', views.PublishRentSeasonListView.as_view(), name='publish_rent_season_list'),

    path('panel/contacts/', views.PropertyContactListView.as_view(), name='contact_property_list'),
    path('panel/propiedades/', views.PropertyListView.as_view(), name='property_custom_list'),

    ## REALTOR
    path('realtor/', views.RealtorListView.as_view(), name='realtor_list'),
    path('realtor/create/', views.RealtorCreateView.as_view(), name='realtor_create'),
    path('realtor/<int:pk>/detail/', views.RealtorDetailView.as_view(), name='realtor_detail'),
    path('realtor/<int:pk>/update/', views.RealtorUpdateView.as_view(), name='realtor_update'),

    ## OWNER
    path('owner/', views.OwnerListView.as_view(), name='owner_list'),
    path('owner/create/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('owner/<int:pk>/update/', views.OwnerUpdateView.as_view(), name='owner_update'),

    ## PROPERTY
    path('<str:property_type>/<str:publish_type>/create/', views.property_create, name='property_create'),
    path('<slug:slug>/<uuid:uuid>/update/', views.property_update, name='property_update'),
    path('select/', views.property_select, name='property_select'),

    ## PUBLICATION
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('<slug:slug>/<uuid:uuid>/publication/create/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('<int:pk>/publication/update/', views.PublicationUpdateView.as_view(), name='publication_update'),
    
    ## GALERY
    path('galery/<slug:slug>/<uuid:uuid>/', views.PropertyGaleryView.as_view(), name='property_galery'),
    path('success/<slug:slug>/<uuid:uuid>/', views.PropertySuccessDetailView.as_view(), name='property_success'),
    
    ## RESULTADOS 
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/', views.custom_list, name='custom_list'),
    path('<str:first_data>/<str:second_data>/', views.custom_list_publish_property, name='custom_list_publish_property'),
    path('<str:publish_type>/', views.custom_list_publish, name='custom_list_publish'),

    #1
    path('property-list/<int:page_number>/<str:publish_type>/<str:property_type>/<str:location_slug>', views.property_list, name='property_list'),
    #2
    path('property-list_publish_property/<int:page_number>/<str:first_data>/<str:second_data>', views.property_list_publish_property, name='property_list_publish_property'),
    #3
    path('property-list_publish/<int:page_number>/<str:publish_type>', views.property_list_publish, name='property_list_publish'),

    
]

hxpatterns = [
    ## PROPERTY
    path('<uuid:uuid>/property/delete', views.PropertyDeleteView.as_view(), name='property_delete'),
    path('property/table', views.TablePropertyView.as_view(), name='table_property'),
    path('<int:pk>/property/active', views.PropertyIsActiveView.as_view(), name='property_active'),

    # GENERAL TABLE
    path('<int:pk>/publication/delete', views.PublicationDeleteView.as_view(), name='publication_delete'),
    path('publication/table', views.TablePublicationView.as_view(), name='table_publication'),
    path('<int:pk>/publication/change', views.PublicationChangeView.as_view(), name='publication_change'),

    ## CREATE AND UPDATE
    path('commune-select', views.commune_select, name='commune_select'),
    path('realtor/create', views.realtor_create, name='realtor_create'),
    path('realtor-select', views.realtor_select, name='realtor_select'),
    path('owner/create', views.owner_create, name='owner_create'),
    path('owner-select', views.owner_select, name='owner_select'),

    ## DETAIL
    path('contact-detail-form/<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.contact_detail_form, name='contact_detail_form'),

    ## CONTACT 
    path('contact/table-contact/<int:page_number>/table', views.TableContactView.as_view(), name='table_contact'),
    path('contact/modal-contact/<int:pk>/<int:page_number>/modal', views.ModalContactView.as_view(), name='modal_contact'),

    ## REALTOR 
    path('realtor/<int:page_number>/table', views.TableRealtorView.as_view(), name='table_realtor'),
    path('realtor/<int:pk>/<int:page_number>/delete/', views.RealtorDeleteView.as_view(), name='realtor_delete'),

    ## REALTOR 
    path('owner/<int:page_number>/table', views.TableOwnerView.as_view(), name='table_owner'),
    path('owner/<int:pk>/<int:page_number>/delete/', views.OwnerDeleteView.as_view(), name='owner_delete'),
]

urlpatterns += hxpatterns