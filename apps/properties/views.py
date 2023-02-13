import os
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required # para que me obligue a logiarme en panel de admin cuando quiero ingresar a una vista
from render_block import render_block_to_string

#test decorator
from .decorators import url_custom_list_decorator
from .utils import url_custom_list_publish_property

# manipulate image
from PIL import Image

# remove file storage
from django.core.files.storage import FileSystemStorage

#cache
from django.views.decorators.cache import cache_control

from .filters import PropertyFilter

from .models import (
    Commune, PropertyImage, Property, House,  
    Apartment, PropertyContact, Realtor, 
    Owner, PropertyManager, Office, UrbanSite, 
    Parcel, Cellar, Industrial, Shop
)

from .forms import (
    PropertyForm, HouseForm, ApartmentForm,
    PropertyContactForm, RealtorForm, OwnerForm,
    OfficeForm, UrbanSiteForm, ParcelForm,
    CellarForm, IndustrialForm, ShopForm,
    PropertyRentForm
)


def property_create_test(request, property_type):
    form = PropertyForm(request.POST or None, request.FILES or None, initial={'property_type': property_type})
    communes = Commune.objects.all()
    commune = ''
    disabled = True

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
        disabled = False


    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
        disabled = False

    if property_type == 'ca':
        form_extra = HouseForm(request.POST or None)
    elif property_type == 'de':
        form_extra = ApartmentForm(request.POST or None)
    else:
        raise ViewDoesNotExist('Pagina no encontrada')
        # raise ValueError('Catagoria no encontrada')

    if request.method == 'POST':
        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
                instance = form.save()
                extra_instance = form_extra.save(commit=False)
                extra_instance.property = instance
                extra_instance.save()
                images = request.FILES.getlist('file')
                for i in images:
                    print('entra al for')
                    PropertyImage.objects.create(property=instance, image=i)
                    print('despues de crear')
                return redirect(reverse('properties:property_galery', args=[instance.slug, instance.uuid]))
        # print('llego')
        # print(request.POST)
        # print(request.FILES)
        # images = request.FILES.getlist('file')
        # for i in images:
        #     print(i)
        #     count+=1
        # print(count)
            # PropertyImage.objects.create(property=instance, image=i)
        # try:
        # if form.is_valid() and form_extra.is_valid():
        #     with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
        #         instance = form.save()
        #         extra_instance = form_extra.save(commit=False)
        #         extra_instance.property = instance
        #         extra_instance.save()
        #         # images = request.FILES.getlist('more_images')
        #         # for i in images:
        #         #     PropertyImage.objects.create(property=instance, image=i)
        #         return redirect(reverse('properties:property_galery', args=[instance.slug, instance.uuid]))
        # else:
        #     messages.error(request, form_extra.errors)
        #     messages.error(request, form.errors)
        # except:
        #     pass
            # messages.error(request, form_extra.errors)
            # messages.error(request, form.errors)
    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,
        'disabled': disabled,

        'form_realtor': RealtorForm(),
        'form_owner': OwnerForm(),
    }
    return render(request, 'test2.html', context)


class PaginationMixin:
    paginate_by = 2


# ========== CRUD GESTIÓN ========== |

class ManagmentListView(PaginationMixin, ListView):
    model = Property
    template_name = 'properties/managment_list.html'

    def get_queryset(self):
        return PropertyManager.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_option'] = 'properties:table_managment'
        context['sidebar_title'] = 'Gestión'
        context['sidebar_subtitle'] = 'Registro de acciones en las propiedades!'
        return context


class ManagmentPaidView(View):
    def get(self, request, *args, **kwargs):

        property_managment = get_object_or_404(PropertyManager, id=kwargs['pk'])

        if kwargs['action'] == 'paid':
            property_managment.is_commission_paid = True
            property_managment.save()

        if kwargs['action'] == 'unpaid':
            property_managment.is_commission_paid = False
            property_managment.save()

        property_list = PropertyManager.objects.filter(state=True)
        paginator = Paginator(property_list, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': data, 
            'url_option': 'properties:table_managment'
        }
        html = render_block_to_string('properties/managment_list.html', 'table_list', context)
        return HttpResponse(html)


# partials
class TableManagmentView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        properties_managments = PropertyManager.objects.filter(state=True)
        properties_managments = properties_managments.filter(Q(type_property__icontains=q) | Q(commission_value__icontains=q))
        paginator = Paginator(properties_managments, 2)
        data = paginator.get_page(kwargs['page_number'])
        context = {
            'object_list': data.object_list, 
            'page_obj': data, 
            'q': q,
            'url_option': 'properties:table_managment'
        }
        html = render_block_to_string('properties/managment_list.html', 'table_list', context)
        return HttpResponse(html)


class ManagmentDeleteView(View):
    def delete(self, request, *args, **kwargs):
       
        property_managment = Property.objects.get(id=kwargs['pk'])
        property_managment.state = False
        property_managment.save()
        properties_managments = property_managment.objects.filter(state=True)
        paginator = Paginator(properties_managments, 2)
        data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': data.object_list, 
            'page_obj': data, 
        }
        html = render_block_to_string('properties/managment_list.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD AGENTE ========== |

class RealtorCreateView(CreateView):
    model = Realtor
    # fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    form_class = RealtorForm
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación'
        return context


class RealtorUpdateView(UpdateView):
    model = Realtor
    fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación'
        return context


class RealtorListView(PaginationMixin, ListView):
    model = Realtor
    template_name = 'properties/realtor_list.html'

    def get_queryset(self):
        return  Realtor.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Agentes'
        context['sidebar_subtitle'] = 'Maneja la información de tus agentes!'
        return context


class RealtorDetailView(DetailView):
    model = Realtor
    template_name = 'properties/realtor_detail.html'


# partials
class TableRealtorView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        print('hola')
        realtors = Realtor.objects.filter(state=True)
        realtors = realtors.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        paginator = Paginator(realtors, 1)
        realtors_data = paginator.get_page(kwargs['page_number'])
        print(realtors_data.object_list)
        context = {
            'object_list': realtors_data.object_list, 
            'page_obj': realtors_data, 
            'q': q
        }
        html = render_block_to_string('properties/realtor_list.html', 'table_list', context)
        return HttpResponse(html)


class RealtorDeleteView(View):
    def delete(self, request, *args, **kwargs):
        realtor = Realtor.objects.get(id=kwargs['pk'])
        realtor.state = False
        realtor.save()
        realtors = Realtor.objects.filter(state=True)
        paginator = Paginator(realtors, 1)
        realtors_data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': realtors_data.object_list, 
            'page_obj': realtors_data, 
        }
        html = render_block_to_string('properties/realtor_list.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD PROPIETARIO ========== |

class OwnerCreateView(CreateView):
    model = Owner
    # fields = ['name', 'rut', 'phone1', 'phone2', 'email']
    form_class = OwnerForm
    template_name = 'properties/owner_create.html'
    success_url = reverse_lazy('properties:owner_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación'
        return context


class OwnerUpdateView(UpdateView):
    model = Owner
    fields = ['name', 'rut', 'phone1', 'phone2', 'email']
    template_name = 'properties/owner_create.html'
    success_url = reverse_lazy('properties:owner_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación'
        return context


class OwnerListView(PaginationMixin, ListView):
    model = Owner
    template_name = 'properties/owner_list.html'

    def get_queryset(self):
        return  Owner.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Propietarios'
        context['sidebar_subtitle'] = 'Maneja la información de tus propietarios!'
        return context


# partials
class TableOwnerView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        owners = Owner.objects.filter(state=True)
        owners = owners.filter(Q(name__icontains=q) | Q(rut__icontains=q))
        paginator = Paginator(owners, 1)
        owners_data = paginator.get_page(kwargs['page_number'])
        print(owners_data.object_list)
        context = {
            'object_list': owners_data.object_list, 
            'page_obj': owners_data,
            'q': q
        }
        html = render_block_to_string('properties/owner_list.html', 'table_list', context)
        return HttpResponse(html)


class OwnerDeleteView(View):
    def get(self, request, *args, **kwargs):
        owner = Owner.objects.get(id=kwargs['pk'])
        owner.state = False
        owner.save()
        owners = Owner.objects.filter(state=True)
        paginator = Paginator(owners, 1)
        owners_data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': owners_data.object_list, 
            'page_obj': owners_data, 
        }
        html = render_block_to_string('properties/owner_list.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD CONTACT ========== |

class PropertyContactListView(PaginationMixin, ListView):
    model = PropertyContact
    template_name = 'properties/contact_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Contactos'
        context['sidebar_subtitle'] = 'Maneja la información de contactos de propiedades!'
        return context


class TableContactView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
    
        contact_list = PropertyContact.objects.filter(name__icontains=q)
        print(contact_list)
        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
            'q': q
        }
        html = render_block_to_string('properties/contact_list.html', 'table_list', context)
        return HttpResponse(html)


class ModalContactView(View):
    def get(self, request, *args, **kwargs):
        contact = PropertyContact.objects.get(id=kwargs['pk'])
        contact.state = False
        contact.save()
        contact_list = PropertyContact.objects.all()
        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data,
        }
        html = render_block_to_string('properties/contact_list.html', 'table_list', context)
        return HttpResponse(html)


def contact_detail_form(request, publish_type, property_type, location_slug, slug, uuid):
    form = PropertyContactForm(request.POST or None) # no se puede asignar valor  de inicio a un elemento excluido
    property = Property.objects.get(uuid=uuid, commune__location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)

    if property_type == 'ca':
        property_especific = get_object_or_404(House, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.houses.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'de':
        property_especific = get_object_or_404(Apartment, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.apartments.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'of':
        property_especific = get_object_or_404(Office, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.offices.first().num_offices} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
    elif property_type == 'su':
        property_especific = get_object_or_404(UrbanSite, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.urban_sites.first().num_lot} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
    elif property_type == 'pa':
        property_especific = get_object_or_404(Parcel, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.parcels.first().num_lot} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
    elif property_type == 'bo':
        property_especific = get_object_or_404(Cellar, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.cellars.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'in':
        property_especific = get_object_or_404(Industrial, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.industrials.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'lc':
        property_especific = get_object_or_404(Shop, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.shops.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'


    form.initial['message'] = message
    
    if form.is_valid():
        form.instance.property = property
        form.save() 
        
        context = {
            'form': PropertyContactForm(initial={'message': message}),
            'property': property_especific
        }
        html = render_block_to_string('properties/property_detail.html', 'contact_detail', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'modal-contact-button'
        return response

    context = {
        'property': property_especific,
        'form': form,
    }
    html = render_block_to_string('properties/property_detail.html', 'contact_detail', context)
    return HttpResponse(html)


# ========== CRUD PROPIEDADES VENDIDAS ========== |

class BuyListView(PaginationMixin, ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(status=Property.Status.BUY, state=True)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_buy'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades vendidas!'
        return context


class BuyFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(status=Property.Status.BUY, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_buy'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class BuyStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.status = Property.Status.DRAFT
            property.save()

        if kwargs['action']  == 'publish':
            property.status = Property.Status.PUBLISH
            property.save()

        if kwargs['action']  == 'buy':
            property.status = Property.Status.BUY
            property.save()

        if kwargs['action']  == 'rent':
            property.status = Property.Status.RENT
            property.save()

        if kwargs['action']  == 'rental_season':
            property.status = Property.Status.RENTAL_SEASON
            property.save()

        if kwargs['action']  == 'exchange':
            property.status = Property.Status.EXCHANGE
            property.save()

        property_list = Property.objects.filter(status=Property.Status.BUY, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_buy'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class BuyDeleteView(View):
    def delete(self, request, *args, **kwargs):
        # messages.success(request, "Propiedad eliminada correctamente")
        property = Property.objects.get(uuid=kwargs['uuid'])
        property.state = False
        property.save()
        property_list = Property.objects.filter(status=Property.Status.BUY, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_buy'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableBuyView(View): 
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.BUY, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_buy'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD PROPIEDADES ARRENDADAS ========== |

class RentListView(PaginationMixin, ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(status=Property.Status.RENT, state=True)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_rent'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades arrendadas!'
        return context


class RentFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(status=Property.Status.RENT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rent'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class RentStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.status = Property.Status.DRAFT
            property.save()

        if kwargs['action']  == 'publish':
            property.status = Property.Status.PUBLISH
            property.save()

        if kwargs['action']  == 'buy':
            property.status = Property.Status.BUY
            property.save()

        if kwargs['action']  == 'rent':
            property.status = Property.Status.RENT
            property.save()

        if kwargs['action']  == 'rental_season':
            property.status = Property.Status.RENTAL_SEASON
            property.save()

        if kwargs['action']  == 'exchange':
            property.status = Property.Status.EXCHANGE
            property.save()

        property_list = Property.objects.filter(status=Property.Status.RENT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rent'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class RentDeleteView(View):
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(uuid=kwargs['uuid'])
        property.state = False
        property.save()
        # messages.success(request, "Propiedad eliminada correctamente")
        property_list = Property.objects.filter(status=Property.Status.RENT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rent'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableRentView(View): 
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.RENT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_rent'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD PROPIEDADES ARRENDADAS POR TEMPORADA ========== |

class RentalSeasonListView(PaginationMixin, ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(status=Property.Status.RENTAL_SEASON, state=True)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_rental_season'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades arrendadas por temporada!'
        return context


class RentalSeasonFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(status=Property.Status.RENTAL_SEASON, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rental_season'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class RentalSeasonStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.status = Property.Status.DRAFT
            property.save()

        if kwargs['action']  == 'publish':
            property.status = Property.Status.PUBLISH
            property.save()

        if kwargs['action']  == 'buy':
            property.status = Property.Status.BUY
            property.save()

        if kwargs['action']  == 'rent':
            property.status = Property.Status.RENT
            property.save()

        if kwargs['action']  == 'rental_season':
            property.status = Property.Status.RENTAL_SEASON
            property.save()

        if kwargs['action']  == 'exchange':
            property.status = Property.Status.EXCHANGE
            property.save()

        property_list = Property.objects.filter(status=Property.Status.RENTAL_SEASON, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rental_season'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class RentalSeasonDeleteView(View):
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(uuid=kwargs['uuid'])
        property.state = False
        property.save()
        # messages.success(request, "Propiedad eliminada correctamente")
        property_list = Property.objects.filter(status=Property.Status.RENTAL_SEASON, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_rental_season'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableRentalSeasonView(View): 
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.RENTAL_SEASON, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_rental_season'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD PROPIEDADES PERMUTADAS ========== |

class ExchangeListView(PaginationMixin, ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(status=Property.Status.EXCHANGE, state=True)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_exchange'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades permutadas!'
        return context


class ExchangeFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(status=Property.Status.EXCHANGE, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_exchange'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class ExchangeStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.status = Property.Status.DRAFT
            property.save()

        if kwargs['action']  == 'publish':
            property.status = Property.Status.PUBLISH
            property.save()

        if kwargs['action']  == 'buy':
            property.status = Property.Status.BUY
            property.save()

        if kwargs['action']  == 'rent':
            property.status = Property.Status.RENT
            property.save()

        if kwargs['action']  == 'rental_season':
            property.status = Property.Status.RENTAL_SEASON
            property.save()

        if kwargs['action']  == 'exchange':
            property.status = Property.Status.EXCHANGE
            property.save()

        property_list = Property.objects.filter(status=Property.Status.EXCHANGE, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_exchange'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class ExchangeDeleteView(View):
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(uuid=kwargs['uuid'])
        property.state = False
        property.save()
        # messages.success(request, "Propiedad eliminada correctamente")
        property_list = Property.objects.filter(status=Property.Status.EXCHANGE, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_exchange'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableExchangeView(View): 
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.EXCHANGE, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_exchange'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# ========== CRUD PROPIEDAD DESPUBLICADAS =========== |

class DraftListView(PaginationMixin, ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(status=Property.Status.DRAFT, state=True)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_draft'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades despublicadas!'
        return context


# partials
class DraftFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(status=Property.Status.DRAFT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class DraftStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.status = Property.Status.DRAFT
            property.save()

        if kwargs['action']  == 'publish':
            property.status = Property.Status.PUBLISH
            property.save()

        if kwargs['action']  == 'buy':
            property.status = Property.Status.BUY
            property.save()

        if kwargs['action']  == 'rent':
            property.status = Property.Status.RENT
            property.save()

        if kwargs['action']  == 'rental_season':
            property.status = Property.Status.RENTAL_SEASON
            property.save()

        if kwargs['action']  == 'exchange':
            property.status = Property.Status.EXCHANGE
            property.save()

        property_list = Property.objects.filter(status=Property.Status.DRAFT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class DraftDeleteView(View):
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(uuid=kwargs['uuid'])
        property.state = False
        property.save()
        # messages.success(request, "Propiedad eliminada correctamente")
        property_list = Property.objects.filter(status=Property.Status.DRAFT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableDraftView(View): # probe como pasar template y context con httpresponse en vez de render
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.DRAFT, state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        # template = get_template('properties/partials/property_table.html')
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)
        # return HttpResponse(template.render(context), content_type='html')


# ========== CRUD PROPIEDADES PUBLICADAS ========== |

def property_publish_list(request):
        properties = Property.objects.filter(status=Property.Status.PUBLISH, state=True)
        paginator = Paginator(properties, 2)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data,
            'url_option': 'table_publish',
            'sidebar_title' : 'Propiedades',
            'sidebar_subtitle' : 'Maneja la información de tus propiedades publicadas!',
        }
        return render(request, 'properties/property_custom.html', context)


def publish_featured(request, pk, action, page_number):
    property = get_object_or_404(Property, id=pk)

    if action == 'normal':
        property.is_featured = False
        property.save()

    if action == 'featured':
        property.is_featured = True
        property.save()

    property_list = Property.objects.filter(status=Property.Status.PUBLISH, state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


def publish_status(request, pk, action, page_number):
    property = get_object_or_404(Property, id=pk)

    # match action:
    #     case 'draft':
    #         property.status = Property.Status.DRAFT
    #         property.save()
    #     case 'publish':
    #         property.status = Property.Status.PUBLISH
    #         property.save()
    #     case 'buy':
    #         property.status = Property.Status.BUY
    #         property.save()
    #     case 'rent':
    #         property.status = Property.Status.RENT
    #         property.save()
    #     case 'rental_season':
    #         property.status = Property.Status.RENTAL_SEASON
    #         property.save()
    #     case _:
    #         property.status = Property.Status.EXCHANGE
    #         property.save()

    if action == 'draft':
        property.status = Property.Status.DRAFT
        property.save()

    elif action == 'publish':
        property.status = Property.Status.PUBLISH
        property.save()

    elif action == 'buy':
        property.status = Property.Status.BUY
        property.save()

    elif action == 'rent':
        property.status = Property.Status.RENT
        property.save()

    elif action == 'rental_season':
        property.status = Property.Status.RENTAL_SEASON
        property.save()

    elif action == 'exchange':
        property.status = Property.Status.EXCHANGE
        property.save()

    property_list = Property.objects.filter(status=Property.Status.PUBLISH, state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)

    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)
 

def publish_delete(request, uuid, page_number):
    property = Property.objects.get(uuid=uuid)
    property.delete()
    # property.state = False
    # property.save()
    # Property.objects.get(uuid=uuid).delete()
    # messages.success(request, "Propiedad eliminada correctamente")
    property_list = Property.objects.filter(status=Property.Status.PUBLISH, state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)

    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


# paginator
def table_publish(request, page_number):
    q = request.GET.get('q', '')

    property_list = Property.objects.filter(commune_id__name__icontains=q, status=Property.Status.PUBLISH, state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data, 
        'q': q,
        'url_option': 'table_publish',
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


# =========== GENERAL PROPIEDADES ========== |

class PropertyGaleryView(View):

    """ Galeria para agregar y eliminar imagenes de detalle de propiedad """   

    def delete_image(self, file):
        # ========== DELETE FILES ========== |

        # OBTENER RUTA
        # 1)
        # image = str(property_image.image)
        # 2)
        # image = property_image.image.url
        # 3)
        image = file.image.path
        
        # Check if the image exists
        if os.path.exists(image):
            # ELIMINAR DE LA RUTA
            # 1) Sirve con todas
            fs = FileSystemStorage()
            fs.delete(image)
        else:
            print('Imagen no existe')
            
        file.delete()

        # 2) Solo sirve con "path"
        # if os.path.isfile(image):
        #     os.remove(image)
        #     property_image.delete()
        
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
        property_images = PropertyImage.objects.filter(property=property)
        context = {
            'property_images': property_images,
            'property': property
        }
        return render(request, 'properties/property_galery.html', context)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # action = json.loads(request.body)['action']
            action = request.POST['action']
            if action == 'delete':
                id = request.POST['id']
                property_image = PropertyImage.objects.get(id=id)
                self.delete_image(property_image)
              
                # retornar previsualización personalizada
                property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
                preview_images = PropertyImage.objects.filter(property=property)
                preview_images = [i.toJSON() for i in preview_images]
   
                data['preview_images'] = preview_images

            elif action == 'create':
                property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
                preview_images = PropertyImage.objects.filter(property=property)
                if preview_images.count() <= 10:
                    id = request.POST.get('id')
                    imagen = request.FILES.get('imagen')

                    try:
                        Image.open(imagen)
                    except Exception as e:
                        data['error'] = str(e)
                        print(str(e))
                        return JsonResponse(data, status=400)
                    else:
                        property_image = PropertyImage.objects.create(property_id=id, image=imagen)
                        # retornar previsualización personalizada
                        preview_images = PropertyImage.objects.filter(property=property)
                        preview_images = [i.toJSON() for i in preview_images]


                        data['id'] = property_image.id
                        data['property_image'] = str(property_image.image)
                        data['preview_images'] = preview_images

                else:
                    data['error'] = 'se alcanzo el limite de imagenes para subir'
                    return JsonResponse(data, status=400)
                # return redirect('properties:property_detail', args=[property.publish_type, property.property_type, property.commune.location_slug, property.slug, property.uuid])
            else:
                data['error']  = 'Ha ocurrido un error'
                return JsonResponse(data, status=400)
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
            # return JsonResponse(data, status=400)
        return JsonResponse(data, status=200)


class PropertySuccessDetailView(DetailView):
    model = Property
    template_name = 'properties/property_success.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(slug=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return queryset.filter()

    def post(self, request, slug, uuid):
        action = request.POST.get('action')
        if action == 'publish':
            property = get_object_or_404(self.model, slug=slug, uuid=uuid)
            property.status = self.model.Status.PUBLISH
            property.save()
            return HttpResponseRedirect(reverse('properties:property_detail', args=[property.publish_type, property.property_type, property.commune.location_slug, property.slug, property.uuid]))
        context = {
            'object': self.get_object()
        }
        return render(request, 'properties/property_success.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def property_detail(request, publish_type, property_type, location_slug, slug, uuid):
    form = PropertyContactForm(request.POST or None) # no se puede asignar valor  de inicio a un elemento excluido
    message = None

    property = Property.objects.get(uuid=uuid, commune__location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)
    if property_type == 'ca':
        property_especific = get_object_or_404(House, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.houses.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'de':
        property_especific = get_object_or_404(Apartment, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.apartments.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'of':
        property_especific = get_object_or_404(Office, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.offices.first().num_offices} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
    elif property_type == 'su':
        property_especific = get_object_or_404(UrbanSite, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.urban_sites.first().num_lot} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
         
    elif property_type == 'pa':
        property_especific = get_object_or_404(Parcel, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.parcels.first().num_lot} Lotes En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'bo':
        property_especific = get_object_or_404(Cellar, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.cellars.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'in':
        property_especific = get_object_or_404(Industrial, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.industrials.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'lc':
        property_especific = get_object_or_404(Shop, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.shops.first().num_local} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
    form.initial['message'] = message

    context = {
        'property': property_especific,
        'property_image': property.properties.all(),
        'form': form,
        'wa_message': property.title,
        'wa_number': '56950092733'
    }
    return render(request, 'properties/property_detail.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def property_create(request, property_type, publish_type):
    if publish_type == 'ar' or publish_type == 'at':
        form = PropertyRentForm(
            request.POST or None, request.FILES or None,
            user=request.user, property_type=property_type,
            publish_type=publish_type
        )  # forma mas robusta pasandosela al form y ahi asignandola
    else:
        form = PropertyForm(
            request.POST or None, request.FILES or None,
            user=request.user, property_type=property_type,
            publish_type=publish_type
        )  # forma mas robusta pasandosela al form y ahi asignandola

    communes = Commune.objects.all()
    commune = ''
    disabled = 'disabled'

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
        disabled = ''

    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
        disabled = ''

    if property_type == 'ca':
        form_extra = HouseForm(request.POST or None)
    elif property_type == 'de':
        form_extra = ApartmentForm(request.POST or None)
    elif property_type == 'of':
        form_extra = OfficeForm(request.POST or None)
    elif property_type == 'su':
        form_extra = UrbanSiteForm(request.POST or None)
    elif property_type == 'pa':
        form_extra = ParcelForm(request.POST or None)
    elif property_type == 'bo':
        form_extra = CellarForm(request.POST or None)
    elif property_type == 'in':
        form_extra = IndustrialForm(request.POST or None)
    elif property_type == 'lc':
        form_extra = ShopForm(request.POST or None)
    else:
        return redirect('pages:home')

    try:
        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
                instance = form.save()
                extra_instance = form_extra.save(commit=False)
                extra_instance.property = instance
                extra_instance.save()
                # images = request.FILES.getlist('more_images')
                # for i in images:
                #     PropertyImage.objects.create(property=instance, image=i)
                return redirect(reverse('properties:property_galery', args=[instance.slug, instance.uuid]))
        else:
            # form.initial['commune'] = commune
            print(form.errors)
            # messages.error(request, form_extra.errors)
            # messages.error(request, form.errors)
    except Exception as e:
        print(str(e))
        pass

    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,
        'disabled': disabled,
        
        'form_realtor': RealtorForm(),
        'form_owner': OwnerForm(),

        'title': 'Creación de Propiedad',
        'subtitle': 'Maneje la creación de sus propiedades',
        
        'property_type': property_type
    }
    return render(request, 'properties/property_form.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def property_update(request, slug, uuid):
    property = Property.objects.get(uuid=uuid, slug=slug)

    if property.publish_type == 'ar' or property.publish_type == 'at':
        form = PropertyRentForm(
            request.POST or None, request.FILES or None,
            instance=property
        )  # forma mas robusta pasandosela al form y ahi asignandola
    else:
        form = PropertyForm(
            request.POST or None, request.FILES or None,
            instance=property
        )  # forma mas robusta pasandosela al form y ahi asignandola

    

    # form = PropertyForm(
    #     request.POST or None, request.FILES or None,
    #     instance=property
    # )

    communes = Commune.objects.all()

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
    else:
        communes = communes.filter(region=property.region)

    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
    else:
        commune = property.commune

    if property.property_type == 'ca':
        house = House.objects.get(property=property)
        form_extra = HouseForm(request.POST or None, instance=house)
    elif property.property_type == 'de':
        apartment = Apartment.objects.get(property=property.id)
        form_extra = ApartmentForm(request.POST or None, instance=apartment)
    elif property.property_type == 'of':
        office = Office.objects.get(property=property.id)
        form_extra = OfficeForm(request.POST or None, instance=office)
    elif property.property_type == 'su':
        urban_site = UrbanSite.objects.get(property=property.id)
        form_extra = UrbanSiteForm(request.POST or None, instance=urban_site)
    elif property.property_type == 'pa':
        parcel = Parcel.objects.get(property=property.id)
        form_extra = ParcelForm(request.POST or None, instance=parcel)
    elif property.property_type == 'bo':
        cellar = Cellar.objects.get(property=property.id)
        form_extra = CellarForm(request.POST or None, instance=cellar)
    elif property.property_type == 'in':
        industrial = Industrial.objects.get(property=property.id)
        form_extra = IndustrialForm(request.POST or None, instance=industrial)
    elif property.property_type == 'lc':
        shop = Shop.objects.get(property=property.id)
        form_extra = ShopForm(request.POST or None, instance=shop)
    else:
        return redirect('pages:home')

    try:
        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
                instance = form.save()
                extra_instance = form_extra.save(commit=False)
                extra_instance.property = instance
                extra_instance.save()
                return redirect('properties:property_galery', instance.slug, instance.uuid)
            # else:
            #     messages.error(request, 'ha ocurrido un error')
    except Exception as e:
        print(str(e))
        pass

    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,

        'form_realtor': RealtorForm(),
        'form_owner': OwnerForm(),

        'title': 'Modificación de Propiedad',
        'subtitle': 'Maneje la modificación de sus propiedades',

        'property_type': property.property_type
    }
    return render(request, 'properties/property_form.html', context)


def property_select(request):
    return render(request, 'properties/property_select.html')


def commune_select(request):

    region = request.GET.get('region', '')

    communes = Commune.objects.all()
    if region != '':
        communes = communes.filter(region=region)
        disabled = ''
    else:
        disabled = 'disabled'

    context = {
        'communes': communes,
        'disabled': disabled,
    }
    html = render_block_to_string('properties/property_form.html', 'commune', context)
    return HttpResponse(html)


def realtor_create(request):
    print(request.POST )
    form = RealtorForm(request.POST or None)
    context = {
        'form_realtor': form,
    }
    if form.is_valid():
        form.save()
        context['form_realtor'] = RealtorForm()
        html = render_block_to_string('properties/property_form.html', 'realtor', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'realtor_select'
        return response
        
    html = render_block_to_string('properties/property_form.html', 'realtor', context)
    return HttpResponse(html)


def realtor_select(request):
    realtors = Realtor.objects.last()
    form = PropertyForm(initial={'realtor': realtors.id})

    context = {
        'form': form,
    }
    html = render_block_to_string('properties/property_form.html', 'realtors', context)
    return HttpResponse(html)


def owner_create(request):
    print(request.POST )
    form = OwnerForm(request.POST or None)
    context = {
        'form_owner': form,
    }
    if form.is_valid():
        form.save()
        context['form_owner'] = OwnerForm()
        html = render_block_to_string('properties/property_form.html', 'owner', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'owner_select'
        return response
        
    html = render_block_to_string('properties/property_form.html', 'owner', context)
    return HttpResponse(html)


def owner_select(request):
    owners = Owner.objects.last()
    form = PropertyForm(initial={'owner': owners.id})

    context = {
        'form': form,
    }
    html = render_block_to_string('properties/property_form.html', 'owners', context)
    return HttpResponse(html)


# ========== FBV TESTING ADAPTING PROPERTY LIST ========== |

# 1)
@url_custom_list_decorator
def custom_list(request, publish_type, property_type, location_slug):

    if publish_type == 've':
        entity = f'Ventas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'ar':
        entity = f'Arriendos de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'at':
        entity = f'Arriendos temporada de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'pe':
        entity = f'Permutas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 

    qs = Property.objects.filter(publish_type=publish_type, property_type=property_type, commune__location_slug=location_slug)


    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'publish_type': publish_type,
        'property_type': property_type,
        'location_slug': location_slug,
    }

    return render(request, 'properties/property_list.html', context)


@url_custom_list_decorator
def property_list(request, page_number, publish_type, property_type, location_slug):

    if publish_type == 've':
        entity = f'Ventas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'ar':
        entity = f'Arriendos de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'at':
        entity = f'Arriendos temporada de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'pe':
        entity = f'Permutas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 

    qs = Property.objects.filter(publish_type=publish_type, property_type=property_type, commune__location_slug=location_slug)

    print(request.GET.get('price_option',''))
    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,

        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'price__gte': price__gte,
        'price__lte': price__lte,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'publish_type': publish_type,
        'property_type': property_type,
        'location_slug': location_slug,
    }
    html = render_block_to_string('properties/property_list.html', 'post', context)
    return HttpResponse(html)


# 2)
def custom_list_publish_property(request, first_data, second_data):
    response = url_custom_list_publish_property(first_data, second_data)

    if len(response) == 2:
        qs = response[0]
        entity = response[1]
    else:
        return redirect(response)

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'first_data': first_data,
        'second_data': second_data,
    }

    return render(request, 'properties/property_list_publish_property.html', context)


def property_list_publish_property(request, page_number, first_data, second_data):

    response = url_custom_list_publish_property(first_data, second_data)

    if len(response) == 2:
        qs = response[0]
        entity = response[1]
    else:
        return redirect(response)

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'entity': entity,

        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'price__gte': price__gte,
        'price__lte': price__lte,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'first_data': first_data,
        'second_data': second_data,
    }
    html = render_block_to_string('properties/property_list_publish_property.html', 'post_publish_property', context)
    return HttpResponse(html)


# 3)
def custom_list_publish(request, publish_type):
    print(publish_type)
    try:
        if publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe':
            qs = Property.objects.filter(publish_type=publish_type, state=True)
        else:
            return redirect('pages:home')
    except Exception as e:
        print(str(e))
        return redirect('pages:home')


    if publish_type == 've':
        entity = 'Inmuebles en Venta'
    if publish_type == 'ar':
        entity = 'Inmuebles en Arriendo'
    if publish_type == 'at':
        entity = 'Inmuebles en Arriendo temporada'
    if publish_type == 'pe':
        entity = 'Inmuebles en Permuta'

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'publish_type': publish_type
    }

    return render(request, 'properties/property_list_publish.html', context)


def property_list_publish(request, page_number, publish_type):
    try:
        if publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe':
            qs = Property.objects.filter(publish_type=publish_type, state=True)
        else:
            return redirect('pages:home')
    except Exception as e:
        print(str(e))
        return redirect('pages:home')


    if publish_type == 've':
        entity = 'Inmuebles en Venta'
    if publish_type == 'ar':
        entity = 'Inmuebles en Arriendo'
    if publish_type == 'at':
        entity = 'Inmuebles en Arriendo temporada'
    if publish_type == 'pe':
        entity = 'Inmuebles en Permuta'

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    
    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs
    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,

        'price__gte': price__gte,
        'price__lte': price__lte,
        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'publish_type': publish_type
    }
    html = render_block_to_string('properties/property_list_publish.html', 'post_publish', context)
    return HttpResponse(html)




        # try: 
        #     action  = request.POST['action']
        #     if action == 'delete':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             # property = get_object_or_404(House, id=id)
        #             # property.delete()
        #             # property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             # property = get_object_or_404(House, id=id)
        #             # property.delete()
        #             # property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad eliminada correctamente")
        #     elif action == 'edit':
        #         pass
        #     elif action == 'publish':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             property = get_object_or_404(House, id=id)
        #             property.state = True
        #             property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             property = get_object_or_404(Apartment, id=id)
        #             property.state = True
        #             property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad publicada correctamente")
        #     elif action == 'draft':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             property = get_object_or_404(House, id=id)
        #             property.state = False
        #             property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             property = get_object_or_404(Apartment, id=id)
        #             property.state = False
        #             property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad despublicada correctamente")
        #     else:
        #         messages.error(request, "Ha ocurrido un error")
        # except Exception as e:
        #     messages.alert(request, str(e))
        # return redirect('property_custom')