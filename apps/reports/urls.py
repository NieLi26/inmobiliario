from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('', views.DashboardTemplateView.as_view(), name='dashboard'),

    path('panel/gestion/', views.OperationHistoryListView.as_view(), name='operation_list'),
]


hx_patterns = [
    path('managment/<int:pk>/<int:page_number>/delete/', views.OperationHistoryDeleteView.as_view(), name='operation_delete'),
    path('managment/<int:pk>/<str:action>/<str:page_number>/paid/', views.OperationHistoryPaidView.as_view(), name='operation_paid'),
    path('managment/<int:page_number>/table', views.TableOperationHistoryView.as_view(), name='table_operation'),
]


urlpatterns += hx_patterns
