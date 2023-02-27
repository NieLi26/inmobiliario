from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.db.models import Q


from .models import OperationHistory

from render_block import render_block_to_string
# Create your views here.


class PaginationMixin:
    paginate_by = 2


class DashboardTemplateView(TemplateView):
    """ Se despligan los graficos y tablas """
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Dashboard'
        context['sidebar_subtitle'] = 'Gestiona la información de tus propiedades a traves de graficos'
        return context


# ========== CRUD OPERATION HISTORY ========== |

class OperationHistoryListView(PaginationMixin, ListView):
    model = OperationHistory
    template_name = 'reports/history_list.html'

    def get_queryset(self):
        return OperationHistory.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_option'] = 'reports:table_operation'
        context['sidebar_title'] = 'Gestión'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context

# partials


class OperationHistoryPaidView(View):
    def get(self, request, *args, **kwargs):

        operation_history = get_object_or_404(OperationHistory, id=kwargs['pk'])

        if kwargs['action'] == 'paid':
            operation_history.is_commission_paid = True
            operation_history.save()

        if kwargs['action'] == 'unpaid':
            operation_history.is_commission_paid = False
            operation_history.save()

        operations_history = OperationHistory.objects.filter(state=True)
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': data, 
            'url_option': 'retpors:table_operation'
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)


class TableOperationHistoryView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        operations_history = OperationHistory.objects.filter(state=True)
        operations_history = operations_history.filter(Q(type_property__icontains=q) | Q(commission_value__icontains=q))
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'object_list': data.object_list, 
            'page_obj': data, 
            'q': q,
            'url_option': 'reports:table_operation'
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)


class OperationHistoryDeleteView(View):
    def delete(self, request, *args, **kwargs):
       
        operation_history = OperationHistory.objects.get(id=kwargs['pk'])
        operation_history.state = False
        operation_history.save()
        operations_history = OperationHistory.objects.filter(state=True)
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': data.object_list, 
            'page_obj': data, 
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)
