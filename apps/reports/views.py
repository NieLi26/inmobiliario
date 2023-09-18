from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from django_htmx.http import HttpResponseClientRefresh

from apps.properties.models import Publication, PropertyContact
from apps.pages.models import Contact, OwnerContact
from .models import OperationBuyHistory, OperationRent, PaymentRent
from .forms import (
    OperationBuyHistoryFirstForm,
    OperationBuyHistorySecondForm,
    OperationBuyHistoryUpdateForm,
    OperationRentForm,
    PaymentRentForm
)

from render_block import render_block_to_string
# Create your views here.


class PaginationMixin:
    paginate_by = 2


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    """ Se despligan los graficos y tablas """
    template_name = 'reports/dashboard.html'

    def filtro_mes_actual(self, model):
        queryset = model.objects.filter(created__month=date.today().month)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = Publication.objects.all()
        property_contact = PropertyContact.objects.all() 
        # Todo MENSUAL
        context['venta'] = publication.filter(
            Q(state=True, property__publish_type='ve') |
            Q(state=True, property__publish_type='pe')
        ).count()
        context['arriendo'] = publication.filter(
            Q(state=True, property__publish_type='ar') |
            Q(state=True, property__publish_type='at')
        ).count()
        context['vendidas'] = publication.filter(
            Q(state=False, property__publish_type='ve') |
            Q(state=False, property__publish_type='pe')
        ).count()
        context['arrendadas'] = publication.filter(
            Q(state=False, property__publish_type='ar') |
            Q(state=False, property__publish_type='at')
        ).count()
        # Porcentajes de cierre
        context['cierre_ventas'] = round(context['vendidas'] * 100 / publication.count())
        context['cierre_arriendos'] = round(context['arrendadas'] * 100 / publication.count())
        # Procentaje tasa conversion venta
        property_contact_ventas = property_contact.filter(
            Q(property__publish_type='ve') |
            Q(property__publish_type='pe')
        ).count()
        property_contact_arriendos = property_contact.filter(
            Q(property__publish_type='ar') |
            Q(property__publish_type='at')
        ).count()

        if context['vendidas'] == 0 or property_contact_ventas == 0:
            context['tasa_ventas'] = 0
        else:
            context['tasa_ventas'] = round(context['vendidas'] * 100 / property_contact_ventas)
             
        if context['arrendadas'] == 0 or property_contact_arriendos == 0:
            context['tasa_arriendos'] = 0
        else:
            context['tasa_arriendos'] = round(context['arrendadas'] * 100 / property_contact_arriendos)

        # consultas diarias
        today_property_contact = property_contact.filter(created=date.today()).count()
        today_contact = Contact.objects.filter(created=date.today()).count()
        today_owner_contact = OwnerContact.objects.filter(created=date.today()).count()
        total_today_contacts = today_property_contact + today_contact + today_owner_contact
        context['total_today_contacts'] = total_today_contacts
        # consultas mensuales
        month_property_contact = self.filtro_mes_actual(PropertyContact).count()
        month_contact = self.filtro_mes_actual(Contact).count()
        month_owner_contact = self.filtro_mes_actual(OwnerContact).count()
        # total_month_contacts = month_property_contact + month_contact + month_owner_contact
        # context['total_month_contacts'] = total_month_contacts
        context['month_property_contact'] = month_property_contact
        context['month_contact'] = month_contact
        context['month_owner_contact'] = month_owner_contact
        # cantidad de tipos de publicacion mensual en espera y publicadas
        month_publication_active = publication.filter(state=True, status='pu', created__month=date.today().month)
        context['total_month_ventas'] = month_publication_active.filter(property__publish_type='ve').count()
        context['total_month_permutas'] = month_publication_active.filter(property__publish_type='pe').count()
        context['total_month_arriendos'] = month_publication_active.filter(property__publish_type='ar').count()
        context['total_month_arriendos_temporada'] = month_publication_active.filter(property__publish_type='at').count()
        # total comisiones mensaules cobras o pendientes
        # context['total_paid_comission'] = OperationBuyHistory.objects.filter(created__month=date.today().month, is_commission_paid=True).count()
        # context['total_no_paid_comission'] = OperationBuyHistory.objects.filter(created__month=date.today().month, is_commission_paid=False).count()

        context['sidebar_title'] = 'Dashboard'
        context['sidebar_subtitle'] = 'Gestiona la información de tus propiedades a traves de graficos'
        return context


# ========== OPERATION BUY ========== |

class OperationBuyListCreateView(LoginRequiredMixin, PaginationMixin, ListView):
    model = OperationBuyHistory
    template_name = 'reports/operation_buy_list.html'

    def get(self, request, *args, **kwargs):
        num_roll = request.GET.get('num_roll', '')
        commune = request.GET.get('commune', '')
        print(num_roll)
        print(commune)
        if num_roll or commune:
            operations = OperationBuyHistory.objects.filter(state=False)
            if commune:
                operations = operations.filter(publication__property__commune__name__icontains=commune)
                print(operations)
            if num_roll:
                operations = operations.filter(publication__property__num_roll__icontains=num_roll)
            context = {
                'operations': operations,
                'num_roll': num_roll,
                'commune': commune
            }
            html = render_block_to_string('modules/operation/buy/modal_create.html', 'operation_list', context)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     return OperationBuyHistory.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Gestión Ventas'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context


# partials
class OperationBuyRetrieveUpdateDestroyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # page_number = request.GET.get('page_number', 1)
        complete = request.GET.get('complete', '')
        operation = get_object_or_404(OperationBuyHistory, pk=self.kwargs['pk'])
        form = None
        url_vals = None
        if complete == 'yes':
            form = OperationBuyHistoryUpdateForm(instance=operation)
            url_vals = '{"action": "update", "complete": "yes"}'
        else:
            url_vals = '{"action": "update", "complete": "no"}'
            if operation.total > 0:
                form = OperationBuyHistorySecondForm(instance=operation)
            else:
                form = OperationBuyHistoryFirstForm(instance=operation)
        print(form.instance.signature_sales_document)
        # operation_buy = OperationBuyHistory.objects.filter(state=True)
        # paginator = Paginator(operation_buy, 2)
        # data = paginator.get_page(page_number)
        context = {
            'form_operation_buy': form,
            'url_operation': f"/reports/operation/buy/{self.kwargs['pk']}/",
            'url_vals': url_vals
            # 'page_obj': data,
        }
        html = render_block_to_string('modules/operation/buy/modal_update.html', 'operation_form', context)
        # html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        context = {}
        # data = parse_qs(request.body.decode('utf-8'))
        # action = data['action'][0]
        # page_number = data.get('page_number', 1)[0]
        action = request.POST.get('action')
        complete = request.POST.get('complete', '')
        print('action es ', action)
        page_number = request.POST.get('page_number', 1)

        operation = get_object_or_404(OperationBuyHistory, id=kwargs['pk'])

        # Evita cambiar estado operacion eliminada(state=False)
        if not operation.state:
            if action == 'enable':
                if operation.publication.has_active_operation():
                    context['errors'] = {'Solo puede haber una operaction activa por publicacion'}
                elif not operation.publication.state:
                    context['errors'] = {'Prohibido, la publicacion debe estar activa'}
                else:
                    operation.state = True
                    operation.save()
                    context['success'] = {'Activada Correctamente'}
            elif action == 'update':
                # Solucion parche mientras no integro htmx + messages django + middleware
                return HttpResponseClientRefresh()
            else:
                context['errors'] = {'Solo se puede realizar una accion con una operacion activada'}
        else:
            if action == 'paid':
                operation.is_commission_paid = True
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'unpaid':
                operation.is_commission_paid = False
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'disable':
                operation.state = False
                operation.save()
                context['success'] = {'Desactivada Correctamente'}
            elif action == 'delete':
                operation.state = False
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'update':
                form = None
                url_vals = None
                if complete == 'yes':
                    print('ENTRo')
                    form = OperationBuyHistoryUpdateForm(request.POST, request.FILES, instance=operation)
                    url_vals = '{"action": "update", "complete": "yes"}'
                else:
                    url_vals = '{"action": "update", "complete": "no"}'
                    if operation.total > 0:
                        form = OperationBuyHistorySecondForm(request.POST, request.FILES, instance=operation)
                    else:
                        form = OperationBuyHistoryFirstForm(request.POST, request.FILES, instance=operation)

                if form.is_valid():
                    print('ES valido')
                    form.save()
                    return HttpResponseClientRefresh()
                else:
                    print('No paso validacion')
                    print(form.errors)
                    context['form_operation_buy'] = form
                    context['errors'] = {'No paso Validacion'}
                    context['url_operation'] = f"/reports/operation/buy/{self.kwargs['pk']}/"
                    context['url_vals'] = url_vals
                    html = render_block_to_string('modules/operation/buy/modal_update.html', 'operation_form', context)
                    return HttpResponse(html)

        operations = OperationBuyHistory.objects.all()
        paginator = Paginator(operations, 2)
        data = paginator.get_page(page_number)
        context['page_obj'] = data
        html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
        return HttpResponse(html)

    # def delete(self, request, *args, **kwargs):
    #     print(request.POST.get('page_number'))
    #     # operation_history = OperationBuyHistory.objects.get(id=kwargs['pk'])
    #     # operation_history.state = False
    #     # operation_history.save()
    #     operations_history = OperationBuyHistory.objects.filter(state=True)
    #     paginator = Paginator(operations_history, 2)
    #     data = paginator.get_page(1)

    #     context = {
    #         'page_obj': data,
    #     }
    #     html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
    #     return HttpResponse(html)


class OperationBuyTableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        estado = request.GET.get('estado', '')
        page_number = request.GET.get('page_number', 1)
        operations = OperationBuyHistory.objects.all()
        if estado == 'active':
            operations = operations.filter(state=True)
        if estado == 'archive':
            operations = operations.filter(state=False)
        operations = operations.filter(Q(publication__property__property_type__icontains=q) | Q(publication__commission_value__icontains=q))
        paginator = Paginator(operations, 2)
        data = paginator.get_page(page_number)
        context = {
            'page_obj': data,
            'q': q,
            'estado': estado
        }
        html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
        return HttpResponse(html)


# ========== OPERATION RENT ========== |

class OperationRentListCreateView(LoginRequiredMixin, PaginationMixin, ListView):
    model = OperationRent
    template_name = 'reports/operation_rent_list.html'

    # def get_queryset(self):
    #     return OperationRent.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Gestión Arriendos'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context


# partials
class OperationRentRetrieveUpdateDestroyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        # page_number = request.GET.get('page_number', 1)
        action = request.GET.get('action')
        operation = get_object_or_404(OperationRent, pk=self.kwargs['pk'])
        if action == 'payment_list':
            payment_list = operation.payments_rent.filter(state=True)
            context['payment_list'] = payment_list
            context['form_payment'] = PaymentRentForm()
            context['operation_id'] = operation.id
            html = render_block_to_string('modules/operation/rent/modal_payment.html', 'payment_list', context)
            return HttpResponse(html)
        form = OperationRentForm(instance=operation)
        url_vals = '{"action": "update"}'
        context['form_operation_rent'] = form
        context['url_operation'] = f"/reports/operation/rent/{self.kwargs['pk']}/"
        context['url_vals'] = url_vals

        html = render_block_to_string('modules/operation/rent/modal_update.html', 'operation_form', context)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        context = {}

        action = request.POST.get('action')
        page_number = request.POST.get('page_number', 1)

        operation = get_object_or_404(OperationRent, id=kwargs['pk'])

        # Evita cambiar estado operacion eliminada(state=False)
        if not operation.state:
            if action == 'enable':
                if operation.publication.has_active_operation():
                    context['errors'] = {'Solo puede haber una operaction activa por publicacion'}
                elif not operation.publication.state:
                    context['errors'] = {'Prohibido, la publicacion debe estar activa'}
                else:
                    operation.state = True
                    operation.save()
                    context['success'] = {'Activada Correctamente'}
            elif action == 'update':
                # Solucion parche mientras no integro htmx + messages django + middleware
                return HttpResponseClientRefresh()
            else:
                context['errors'] = {'Solo se puede realizar una accion con una operacion activada'}
        else:
            if action == 'paid':
                operation.is_lease_commission_paid = True
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'unpaid':
                operation.is_lease_commission_paid = False
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'confirm':
                if operation.lease_start_date and operation.lease_final_date:
                    operation.is_completed = True
                    operation.save()
                    context['success'] = {'Realizado Correctamente'}
                else:
                    context['errors'] = {'Faltan datos para poder confirmar'}  
            elif action == 'no_confirm':
                operation.is_completed = False
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'disable':
                operation.state = False
                operation.is_completed = False
                operation.save()
                context['success'] = {'Desactivada Correctamente'}
            elif action == 'delete':
                operation.state = False
                operation.save()
                context['success'] = {'Realizado Correctamente'}
            elif action == 'update':
                form = OperationRentForm(request.POST, request.FILES, instance=operation)
                url_vals = '{"action": "update"}'

                if form.is_valid():
                    form.save()
                    return HttpResponseClientRefresh()
                else:
                    print(form.errors)
                    context['form_operation_rent'] = form
                    context['errors'] = {'No paso Validacion'}
                    context['url_operation'] = f"/reports/operation/rent/{self.kwargs['pk']}/"
                    context['url_vals'] = url_vals
                    html = render_block_to_string('modules/operation/rent/modal_update.html', 'operation_form', context)
                    return HttpResponse(html)

        operations = OperationRent.objects.all()
        paginator = Paginator(operations, 2)
        data = paginator.get_page(page_number)
        context['page_obj'] = data
        html = render_block_to_string('reports/operation_rent_list.html', 'table_list', context)
        return HttpResponse(html)


class OperationRentTableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        estado = request.GET.get('estado', '')
        page_number = request.GET.get('page_number', 1)
        operations = OperationRent.objects.all()
        if estado == 'active':
            operations = operations.filter(state=True)
        if estado == 'archive':
            operations = operations.filter(state=False)
        operations = operations.filter(Q(publication__property__property_type__icontains=q) | Q(publication__commission_value__icontains=q))
        paginator = Paginator(operations, 2)
        data = paginator.get_page(page_number)
        context = {
            'page_obj': data,
            'q': q,
        }
        html = render_block_to_string('reports/operation_rent_list.html', 'table_list', context)
        return HttpResponse(html)


# ========== PAYMENT RENT ========== |

class PaymentRentListCreateView(LoginRequiredMixin, PaginationMixin, ListView):
    model = PaymentRent
    template_name = 'reports/payment_rent_list.html'

    def post(self, request, *args, **kwargs):
        context = {}
        operation_rent = request.POST.get('operation_rent')

        operation = get_object_or_404(OperationRent, pk=operation_rent)

        if operation.state and operation.is_completed and operation.lease_final_date > date.today():
            form = PaymentRentForm(request.POST)
            context['payment_list'] = operation.payments_rent.filter(state=True)
            context['operation_id'] = operation_rent

            if form.is_valid():
                form.save()
                context['form_payment'] = PaymentRentForm()
                context['success'] = {'Pago Guardado Correctamente'}
            else:
                print(form.errors)
                context['form_payment'] = form
                context['errors'] = {'No paso Validacion'}

            html = render_block_to_string('modules/operation/rent/modal_payment.html', 'payment_list', context)
            return HttpResponse(html)
        return HttpResponseClientRefresh()

    def get_queryset(self):
        return PaymentRent.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_payment'] = PaymentRentForm()
        context['sidebar_title'] = 'Gestión Arriendos'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context


# partials
class PaymentRentRetrieveUpdateDestroyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        # page_number = request.GET.get('page_number', 1)
        action = request.GET.get('action')
        operation_id = request.GET.get('operation_id')
        payment_rent = get_object_or_404(PaymentRent, pk=self.kwargs['pk'])

        if operation_id:
            operation = get_object_or_404(OperationRent, pk=operation_id)
            if operation.state and operation.is_completed:
                if action == 'update':
                    context['payment_list'] = operation.payments_rent.filter(state=True)
                    context['form_payment'] = PaymentRentForm(instance=payment_rent)
                    context['operation_id'] = operation_id
                    context['action'] = 'update'
                    context['url_payment'] = f"/reports/operation/rent/payment/{self.kwargs['pk']}/"
                    html = render_block_to_string('modules/operation/rent/modal_payment.html', 'payment_list', context)
                    return HttpResponse(html)
            else:
                return HttpResponseClientRefresh()
            
        context['payment_rent'] = payment_rent
        html = render_block_to_string('modules/operation/payment_rent/modal_update.html', 'operation_form', context)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        context = {}

        action = request.POST.get('action')
        operation_rent = request.POST.get('operation_rent')
        page_number = request.POST.get('page_number', 1)

        payment_rent = get_object_or_404(PaymentRent, id=kwargs['pk'])

        if operation_rent:
            operation = get_object_or_404(OperationRent, pk=operation_rent)
            if operation.state and operation.is_completed and operation.lease_final_date > date.today():
                payment_list = operation.payments_rent.filter(state=True)
                context['payment_list'] = payment_list

                if action == 'delete':
                    context['form_payment'] = PaymentRentForm()
                    payment_rent.state = False
                    payment_rent.save()
                elif action == 'update':
                    print('ENTROO O NO')
                    form = PaymentRentForm(request.POST, request.FILES, instance=payment_rent)

                    if form.is_valid():
                        form.save()
                        context['form_payment'] = PaymentRentForm()
                    else:
                        print(form.errors)
                        print('SE equivoco la actualizacion')
                        context['errors'] = {'No paso Validacion'}
                        context['action'] = 'update'
                        context['form_payment'] = form
                        context['url_payment'] = f"/reports/operation/rent/payment/{self.kwargs['pk']}/"
                context['operation_id'] = operation_rent
                html = render_block_to_string('modules/operation/rent/modal_payment.html', 'payment_list', context)
                return HttpResponse(html)
            else:
                return HttpResponseClientRefresh()
        else:
            if action == 'paid':
                payment_rent.is_commission_paid = True
                payment_rent.save()
            elif action == 'unpaid':
                payment_rent.is_commission_paid = False
                payment_rent.save()
            elif action == 'delete':
                payment_rent.state = False
                payment_rent.save()
            elif action == 'update':
                form = PaymentRentForm(request.POST, request.FILES, instance=payment_rent)
                url_vals = '{"action": "update"}'

                if form.is_valid():
                    form.save()
                    return HttpResponseClientRefresh()
                else:
                    print(form.errors)
                    context['form_payment_rent'] = form
                    context['errors'] = {'No paso Validacion'}
                    context['url_operation'] = f"/reports/operation/rent/payment/{self.kwargs['pk']}/"
                    context['url_vals'] = url_vals
                    html = render_block_to_string('modules/operation/payment_rent/modal_update.html', 'operation_form', context)
                    return HttpResponse(html)

        payments_rent = PaymentRent.objects.filter(state=True)
        paginator = Paginator(payments_rent, 2)
        data = paginator.get_page(page_number)
        context['page_obj'] = data
        html = render_block_to_string('reports/payment_rent_list.html', 'table_list', context)
        return HttpResponse(html)


def hx_publication_buy_list(request):
    context = {}
    publication_list = Publication.objects.filter(
            status=Publication.Status.PUBLISH, state=True,
            property__publish_type='ve'
        )
    paginator = Paginator(publication_list, 2)
    data = paginator.get_page(1)
    context['page_obj'] = data
    context['publish_type'] = 've'
    context['form_operation_buy'] = OperationBuyHistoryForm()
    context['success'] = {'Operacion Realizada Correctamente'}
    html = render_block_to_string('properties/publication_list.html', 'table_list', context)
    return HttpResponse(html)

