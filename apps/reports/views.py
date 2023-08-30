from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from django_htmx.http import HttpResponseClientRefresh

from apps.properties.models import Publication, PropertyContact
from apps.pages.models import Contact, OwnerContact
from .models import OperationBuyHistory
from .forms import OperationBuyHistoryForm, OperationBuyHistoryUpdateForm

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
            Q(operation='wa', property__publish_type='ve') |
            Q(operation='wa', property__publish_type='pe')
        ).count()
        context['arriendo'] = publication.filter(
            Q(operation='wa', property__publish_type='ar') |
            Q(operation='wa', property__publish_type='at')
        ).count()
        context['vendidas'] = publication.filter(
            Q(operation='fi', property__publish_type='ve') |
            Q(operation='fi', property__publish_type='pe')
        ).count()
        context['arrendadas'] = publication.filter(
            Q(operation='fi', property__publish_type='ar') |
            Q(operation='fi', property__publish_type='at')
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
        month_publication_active = publication.filter(operation='wa', status='pu', created__month=date.today().month)
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


# ========== CRUD OPERATION VENTA HISTORY ========== |

# class OperationHistoryBuyListView(LoginRequiredMixin, PaginationMixin, ListView):
#     model = OperationHistory
#     template_name = 'reports/history_list.html'

#     def get_queryset(self):
#         return OperationHistory.objects.filter(state=True, property__property_type='ca')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['url_option'] = 'reports:table_operation'
#         context['sidebar_title'] = 'Gestión'
#         context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
#         return context

# ========== CRUD OPERATION HISTORY ========== |

class OperationBuyListCreateView(LoginRequiredMixin, PaginationMixin, ListView):
    model = OperationBuyHistory
    template_name = 'reports/operation_buy_list.html'

    def post(self, request, *args, **kwargs):
        context = {}
        form = OperationBuyHistoryForm(request.POST, request.FILES)
        print('entro')
        if form.is_valid():
            print('paso valdiacion')
            form.save()
            return HttpResponseClientRefresh()
        else:
            print('No paso validacion')
            print(form.errors)
            context['form_operation_buy'] = form
            context['errors'] = {'No paso Validacion'}
        html = render_block_to_string('modules/operation/modal_buy_create.html', 'operation_form', context)
        return HttpResponse(html)

    def get_queryset(self):
        return OperationBuyHistory.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['url_option'] = 'reports:table_operation'
        # property_type = [
        #     {'name': 'ca', 'value': 'Casa'},
        #     {'name': 'de', 'value': 'Departamento'},
        #     {'name': 'of', 'value': 'Oficina'},
        #     {'name': 'lc', 'value': 'Local Comercial'},
        #     {'name': 'su', 'value': 'Sitio Urbano'},
        #     {'name': 'in', 'value': 'Industrial'},
        #     {'name': 'bo', 'value': 'Bodega'},
        #     {'name': 'pa', 'value': 'Parcela'}
        # ]

        # publish_type = [
        #     {'name': 've', 'value': 'Venta'},
        #     {'name': 'pe', 'value': 'Permuta'},
        #     {'name': 'ar', 'value': 'Arriendo'},
        #     {'name': 'at', 'value': 'Arriendo Temporada'}
        # ]
        # context['property_type'] = property_type
        # context['publish_type'] = publish_type
        # context['form_operation_buy'] = OperationBuyHistoryUpdateForm()
        context['sidebar_title'] = 'Gestión'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context


# partials
class OperationRetrieveUpdateDestroyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page_number', 1)
        operation = OperationBuyHistory.objects.get(pk=self.kwargs['pk'])
        print('existe ', operation)

        operation_buy = OperationBuyHistory.objects.filter(state=True)
        paginator = Paginator(operation_buy, 2)
        data = paginator.get_page(page_number)
        context = {
            'form_operation_buy': OperationBuyHistoryUpdateForm(instance=operation),
            'url_operation': f"/reports/operation/buy/{self.kwargs['pk']}/"
            # 'page_obj': data,
        }
        html = render_block_to_string('modules/operation/modal_buy_update.html', 'operation_form', context)
        # html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        context = {}
        # data = parse_qs(request.body.decode('utf-8'))
        # action = data['action'][0]
        # page_number = data.get('page_number', 1)[0]
        action = request.POST.get('action')
        print('action es ', action)
        page_number = request.POST.get('page_number', 1)

        operation_buy = get_object_or_404(OperationBuyHistory, id=kwargs['pk'])

        if action == 'paid':
            operation_buy.is_commission_paid = True
            operation_buy.save()
        elif action == 'unpaid':
            operation_buy.is_commission_paid = False
            operation_buy.save()
        elif action == 'delete':
            operation_buy.state = False
            operation_buy.save()
        elif action == 'update':
            print(request.FILES)
            form = OperationBuyHistoryUpdateForm(request.POST, request.FILES, instance=operation_buy)
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
                html = render_block_to_string('modules/operation/modal_buy_update.html', 'operation_form', context)
                return HttpResponse(html)

        operation_buy = OperationBuyHistory.objects.filter(state=True)
        paginator = Paginator(operation_buy, 2)
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
        page_number = request.GET.get('page_number', 1)
        operations_buy = OperationBuyHistory.objects.filter(state=True)
        operations_buy = operations_buy.filter(Q(publication__property__property_type__icontains=q) | Q(publication__commission_value__icontains=q))
        paginator = Paginator(operations_buy, 2)
        data = paginator.get_page(page_number)
        context = {
            'page_obj': data,
            'q': q,
        }
        html = render_block_to_string('reports/operation_buy_list.html', 'table_list', context)
        return HttpResponse(html)


# class OperationBuyHistoryCreateView(LoginRequiredMixin, PaginationMixin, View):
#     def post(self, request, *args, **kwargs):
#         context = {}
#         form = OperationBuyHistoryForm(request.POST)
#         print('entro')
#         if form.is_valid():
#             print('paso valdiacion')
#             form.save()

#             return HttpResponseClientRefresh()


#             # OPCION 1
#             # response = render(request, "properties/publication_list.html")
#             # return trigger_client_event(
#             #     response,
#             #     "operation-buy",
#             #     after="swap"
#             # )

#             # OPCION 1.1

#             # response = HttpResponse('')
#             # response['HX-Trigger'] = 'operation-buy'
#             # return response

#             # OPCION 2
#             # publication_list = Publication.objects.filter(
#             #         status=Publication.Status.PUBLISH, state=True,
#             #         property__publish_type='ve'
#             #     )
#             # paginator = Paginator(publication_list, 2)
#             # data = paginator.get_page(1)
#             # context['page_obj'] = data
#             # context['publish_type'] = 've'
#             # context['form_operation_buy'] = OperationBuyHistoryForm()
#             # context['success'] = {'Operacion Realizada Correctamente'}

#             # html = render_block_to_string('properties/publication_list.html', 'table_list', context)
#             # response = HttpResponse(html)
#             # response["HX-Retarget"] = '#custom_table'
#             # return response
#         else:
#             print('No paso validacion')
#             print(form.errors)
#             context['form_operation_buy'] = form
#             context['errors'] = {'No paso Validacion'}
#         html = render_block_to_string('modules/publication/modal_create_operation_buy.html', 'operation_form', context)
#         return HttpResponse(html)


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


# def contact_detail_form(request, publish_type, property_type, location_slug, slug, uuid):
#     form = PropertyContactForm(request.POST or None) # no se puede asignar valor  de inicio a un elemento excluido
#     property = Property.objects.get(uuid=uuid, commune__location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)

#     if property_type == 'ca':
#         property_especific = get_object_or_404(House, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.houses.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

#     elif property_type == 'de':
#         property_especific = get_object_or_404(Apartment, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.apartments.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

#     elif property_type == 'of':
#         property_especific = get_object_or_404(Office, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.offices.first().num_offices} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
#     elif property_type == 'su':
#         property_especific = get_object_or_404(UrbanSite, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.urban_sites.first().num_lot} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
#     elif property_type == 'pa':
#         property_especific = get_object_or_404(Parcel, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.parcels.first().num_lot} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
#     elif property_type == 'bo':
#         property_especific = get_object_or_404(Cellar, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.cellars.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

#     elif property_type == 'in':
#         property_especific = get_object_or_404(Industrial, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.industrials.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

#     elif property_type == 'lc':
#         property_especific = get_object_or_404(Shop, property=property)
#         message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.shops.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

#     form.initial['message'] = message
    
#     if form.is_valid():
#         form.instance.property = property
#         form.save()
    
#         context = {
#             'form': PropertyContactForm(initial={'message': message}),
#             'property': property_especific,
#             'success': {'Mensaje enviado correctamente'}
#         }
#         html = render_block_to_string('properties/publication_detail.html', 'contact_detail', context)
#         response = HttpResponse(html)
#         response['HX-Trigger'] = 'modal-contact-button'
#         return response
#     context = {
#         'property': property_especific,
#         'form': form,
#         # 'errors': form.errors
#     }
#     html = render_block_to_string('properties/publication_detail.html', 'contact_detail', context)
#     return HttpResponse(html)

# partials
class OperationHistoryPaidView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        operation_history = get_object_or_404(OperationBuyHistory, id=kwargs['pk'])

        if kwargs['action'] == 'paid':
            operation_history.is_commission_paid = True
            operation_history.save()

        if kwargs['action'] == 'unpaid':
            operation_history.is_commission_paid = False
            operation_history.save()

        operations_history = OperationBuyHistory.objects.filter(state=True)
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': data,
            'url_option': 'retpors:table_operation'
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)


class TableOperationHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        operations_history = OperationBuyHistory.objects.filter(state=True)
        operations_history = operations_history.filter(Q(publication__property__property_type__icontains=q) | Q(publication__commission_value__icontains=q))
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'object_list': data.object_list, 
            'page_obj': data, 
            'q': q,
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)


class OperationHistoryDeleteView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
    
        operation_history = OperationBuyHistory.objects.get(id=kwargs['pk'])
        operation_history.state = False
        operation_history.save()
        operations_history = OperationBuyHistory.objects.filter(state=True)
        paginator = Paginator(operations_history, 2)
        data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': data.object_list,
            'page_obj': data, 
        }
        html = render_block_to_string('reports/history_list.html', 'table_list', context)
        return HttpResponse(html)

