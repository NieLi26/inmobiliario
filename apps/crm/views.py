from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django_htmx.http import HttpResponseClientRefresh
from render_block import render_block_to_string
from .models import Client
from .forms import ClientForm


class PaginationMixin:
    paginate_by = 2


# Create your views here.
class ClientListCreateView(PaginationMixin, ListView):
    model = Client
    # context_object_name = 'clients'
    template_name = 'crm/client_list.html'

    def post(self, request, *args, **kwargs):
        context = {}
        action = request.POST.get('action')
        form = ClientForm(request.POST)
        if action == 'new_form':
            context['form'] = ClientForm()
        else:
            if form.is_valid():
                form.save()
                # FORMA 1 recarga normal
                # return HttpResponseClientRefresh()

                # FORMA 2 recarga tabla y resetear formulario
                # context['form'] = ClientForm()
                # html = render_block_to_string('modules/client/modal_form.html', 'client_form', context)
                # response = HttpResponse(html)

                # FORMA # recarga tabla y cierra formulario
                response = HttpResponse(status=204)
                response['HX-Trigger'] = 'clientListReload'
                return response
            context['form'] = form
        html = render_block_to_string('modules/client/modal_form.html', 'client_form', context)
        return HttpResponse(html)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = ClientForm()
        return context


# paginator
class TableClientView(LoginRequiredMixin, View):  # probe como pasar template y context con httpresponse en vez de render
    def get(sefl, request, *args, **kwargs):
        context = {}
        q = request.GET.get('q', '')
        page_number = request.GET.get('page_number', 1)

        clients = Client.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

        paginator = Paginator(clients, 2)
        data = paginator.get_page(page_number)

        context['page_obj'] = data
        context['q'] = q
        html = render_block_to_string('crm/client_list.html', 'table_list', context)
        return HttpResponse(html)


class ClientRetrieveUpdateDestroyView(View):
    def get(sefl, request, *args, **kwargs):
        context = {}
        action = request.GET.get('action')

        client = get_object_or_404(Client, pk=kwargs['pk'])

        if action == 'update_form':
            context['form'] = ClientForm(instance=client)
            context['url_vals'] = '{"action": "update"}'
            context['url_form'] = f"/crm/clients/{kwargs['pk']}/"
            html = render_block_to_string('modules/client/modal_form.html', 'client_form', context)
            return HttpResponse(html)
        context['client'] = client
        html = render_block_to_string('modules/client/modal_detail.html', 'client_detail', context)
        return HttpResponse(html)

    def post(sefl, request, *args, **kwargs):
        context = {}
        q = request.POST.get('q', '')
        page_number = request.POST.get('page_number', 1)
        action = request.POST.get('action')

        client = get_object_or_404(Client, pk=kwargs['pk'])

        if action == 'delete':
            pass
            # client.delete()
        elif action == 'disable':
            client.state = False
        elif action == 'enable':
            client.state = True
        elif action == 'update':
            form = ClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                response = HttpResponse(status=204)
                response['HX-Trigger'] = 'clientListReload'
                return response
            context['form'] = form
            context['url_vals'] = '{"action": "update"}'
            context['url_form'] = f"/crm/clients/{kwargs['pk']}/"
            html = render_block_to_string('modules/client/modal_form.html', 'client_form', context)
            return HttpResponse(html)

        clients = Client.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )
        paginator = Paginator(clients, 2)
        data = paginator.get_page(page_number)

        context['page_obj'] = data
        context['q'] = q
        html = render_block_to_string('crm/client_list.html', 'table_list', context)
        return HttpResponse(html)
