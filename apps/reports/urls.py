from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('', views.DashboardTemplateView.as_view(), name='dashboard'),
    path('operation/buy/', views.OperationBuyListCreateView.as_view(), name='operation_buy_list'),
    path('operation/rent/', views.OperationRentListCreateView.as_view(), name='operation_rent_list'),
    path('operation/rent/payment/', views.PaymentRentListCreateView.as_view(), name='payment_rent_list'),
]

hx_patterns = [
    # VENTA
    path('operation/buy/table', views.OperationBuyTableView.as_view(), name='operation_buy_table'),
    path('operation/buy/<int:pk>/', views.OperationBuyRetrieveUpdateDestroyView.as_view(), name='operation_buy_detail'),
    # ARRIENDO
    path('operation/rent/table', views.OperationRentTableView.as_view(), name='operation_rent_table'),
    path('operation/rent/<int:pk>/', views.OperationRentRetrieveUpdateDestroyView.as_view(), name='operation_rent_detail'),
    # PAGO ARRIENDO
    path('operation/rent/payment/<int:pk>/', views.PaymentRentRetrieveUpdateDestroyView.as_view(), name='payment_rent_detail'),

    # path('hx_publication_buy_list/', views.hx_publication_buy_list, name='hx_publication_buy_list'),
]

urlpatterns += hx_patterns
