from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('', views.DashboardTemplateView.as_view(), name='dashboard'),

    path('operation/buy/', views.OperationBuyListCreateView.as_view(), name='operation_buy_list'),
]


hx_patterns = [
    # path('operation/buy/create', views.OperationBuyHistoryCreateView.as_view(), name='operation_buy_create'),

    # path('managment/<int:pk>/<int:page_number>/delete/', views.OperationHistoryDeleteView.as_view(), name='operation_delete'),
    # path('managment/<int:pk>/<str:action>/<str:page_number>/paid/', views.OperationHistoryPaidView.as_view(), name='operation_paid'),
    
    path('operation/buy/table', views.OperationBuyTableView.as_view(), name='operation_buy_table'),
    path('operation/buy/<int:pk>/', views.OperationRetrieveUpdateDestroyView.as_view(), name='operation_buy_detail'),
    # path('managment/<int:page_number>/table', views.TableOperationHistoryView.as_view(), name='table_operation'),

    path('hx_publication_buy_list/', views.hx_publication_buy_list, name='hx_publication_buy_list'),
]


urlpatterns += hx_patterns
