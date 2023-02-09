from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    # Test
    path('<str:property_type>/create/test/', views.property_create_test, name='property_create_test'),
    

    ## PANEL
    path('panel/publicaciones/', views.property_publish_list, name='property_custom_publish'), 
    path('panel/despublicaciones/', views.DraftListView.as_view(), name='property_custom_draft'), 
    path('panel/vendidas/', views.BuyListView.as_view(), name='property_custom_buy'), 
    path('panel/arrendadas/', views.RentListView.as_view(), name='property_custom_rent'), 
    path('panel/arrendadas-temporada/', views.RentalSeasonListView.as_view(), name='property_custom_rental_season'), 
    path('panel/permutadas/', views.ExchangeListView.as_view(), name='property_custom_exchange'), 
    path('panel/contacts/', views.PropertyContactListView.as_view(), name='contact_property_list'),
    path('panel/gestion/', views.ManagmentListView.as_view(), name='managment_list'),

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
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.property_detail, name='property_detail'),
    path('<str:property_type>/create/', views.property_create, name='property_create'),
    path('<slug:slug>/<uuid:uuid>/update/', views.property_update, name='property_update'),
    path('select/', views.property_select, name='property_select'),
    
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
    ## MANAGMENT
    path('managment/<int:pk>/<int:page_number>/delete/', views.ManagmentDeleteView.as_view(), name='managment_delete'),
    path('managment/<int:pk>/<str:action>/<str:page_number>/paid/', views.ManagmentPaidView.as_view(), name='managment_paid'),
    path('managment/<int:page_number>/table', views.TableManagmentView.as_view(), name='table_managment'),
    
    ## PUBLISH
    path('publish/<uuid:uuid>/<int:page_number>/delete', views.publish_delete, name='publish_delete'),
    path('publish/<int:pk>/<str:action>/<str:page_number>/status', views.publish_status, name='publish_status'),
    path('publish/<int:pk>/<str:action>/<str:page_number>/fatured', views.publish_featured, name='publish_featured'),
    path('publish/<int:page_number>/table', views.table_publish, name='table_publish'),

    ## DRAFT
    path('draft/<uuid:uuid>/<int:page_number>/delete/', views.DraftDeleteView.as_view(), name='draft_delete'),
    path('draft/<int:pk>/<str:action>/<str:page_number>/status/', views.DraftStatusView.as_view(), name='draft_status'),
    path('draft/<int:pk>/<str:action>/<str:page_number>/featured/', views.DraftFeaturedView.as_view(), name='draft_featured'),
    path('draft/<int:page_number>/table', views.TableDraftView.as_view(), name='table_draft'),

    ## BUY
    path('buy/<uuid:uuid>/<int:page_number>/delete/', views.BuyDeleteView.as_view(), name='buy_delete'),
    path('buy/<int:pk>/<str:action>/<str:page_number>/status/', views.BuyStatusView.as_view(), name='buy_status'),
    path('buy/<int:pk>/<str:action>/<str:page_number>/featured/', views.BuyFeaturedView.as_view(), name='buy_featured'),
    path('buy/<int:page_number>/table', views.TableBuyView.as_view(), name='table_buy'),

    ## RENT
    path('rent/<uuid:uuid>/<int:page_number>/delete/', views.RentDeleteView.as_view(), name='rent_delete'),
    path('rent/<int:pk>/<str:action>/<str:page_number>/status/', views.RentStatusView.as_view(), name='rent_status'),
    path('rent/<int:pk>/<str:action>/<str:page_number>/featured/', views.RentFeaturedView.as_view(), name='rent_featured'),
    path('rent/<int:page_number>/table', views.TableRentView.as_view(), name='table_rent'),

    ## RENTAL SEASON
    path('rental-season/<uuid:uuid>/<int:page_number>/delete/', views.RentalSeasonDeleteView.as_view(), name='rental_season_delete'),
    path('rental-season/<int:pk>/<str:action>/<str:page_number>/status/', views.RentalSeasonStatusView.as_view(), name='rental_season_status'),
    path('rental-season/<int:pk>/<str:action>/<str:page_number>/featured/', views.RentalSeasonFeaturedView.as_view(), name='rental_season_featured'),
    path('rental-season/<int:page_number>/table', views.TableRentalSeasonView.as_view(), name='table_rental_season'),

    ## EXCHANGE
    path('exchange/<uuid:uuid>/<int:page_number>/delete/', views.ExchangeDeleteView.as_view(), name='exchange_delete'),
    path('exchange/<int:pk>/<str:action>/<str:page_number>/status/', views.ExchangeStatusView.as_view(), name='exchange_status'),
    path('exchange/<int:pk>/<str:action>/<str:page_number>/featured/', views.ExchangeFeaturedView.as_view(), name='exchange_featured'),
    path('exchange/<int:page_number>/table', views.TableExchangeView.as_view(), name='table_exchange'),

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