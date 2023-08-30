import os
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required # para que me obligue a logiarme en panel de admin cuando quiero ingresar a una vista
from render_block import render_block_to_string

#test decorator
from .decorators import url_custom_list_decorator
from .utils import url_custom_list_publish_property, get_ip

# manipulate image
from PIL import Image

# remove file storage
from django.core.files.storage import FileSystemStorage

# cache FBV
from django.views.decorators.cache import cache_control
# cache CBV
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .filters import PropertyFilter

from .models import (
    Commune, PropertyImage, Property, House,  
    Apartment, PropertyContact, Realtor, 
    Owner, Office, UrbanSite, 
    Parcel, Cellar, Industrial, Shop, IpVisitor,
    Publication
)

from .forms import (
    PropertyForm, HouseForm, ApartmentForm,
    PropertyContactForm, RealtorForm, OwnerForm,
    OfficeForm, UrbanSiteForm, ParcelForm,
    CellarForm, IndustrialForm, ShopForm,
    PropertyRentForm, PublicationForm,
    PublicationRentForm
)

from apps.reports.forms import OperationBuyHistoryForm


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


# ========== CRUD AGENTE ========== |

class RealtorCreateView(LoginRequiredMixin, CreateView):
    model = Realtor
    # fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    form_class = RealtorForm
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación'
        return context


class RealtorUpdateView(LoginRequiredMixin, UpdateView):
    model = Realtor
    fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación'
        return context


class RealtorListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Realtor
    template_name = 'properties/realtor_list.html'

    def get_queryset(self):
        return Realtor.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Agentes'
        context['sidebar_subtitle'] = 'Maneja la información de tus agentes!'
        return context


class RealtorDetailView(LoginRequiredMixin, DetailView):
    model = Realtor
    template_name = 'properties/realtor_detail.html'


# partials
class TableRealtorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')

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


class RealtorDeleteView(LoginRequiredMixin, View):
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

class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    # fields = ['name', 'rut', 'phone1', 'phone2', 'email']
    form_class = OwnerForm
    template_name = 'properties/owner_create.html'
    success_url = reverse_lazy('properties:owner_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación'
        return context


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    fields = ['name', 'rut', 'phone1', 'phone2', 'email']
    template_name = 'properties/owner_create.html'
    success_url = reverse_lazy('properties:owner_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación'
        return context


class OwnerListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Owner
    template_name = 'properties/owner_list.html'

    def get_queryset(self):
        return Owner.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Propietarios'
        context['sidebar_subtitle'] = 'Maneja la información de tus propietarios!'
        return context


# partials
class TableOwnerView(LoginRequiredMixin, View):
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


class OwnerDeleteView(LoginRequiredMixin, View):
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

class PropertyContactListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = PropertyContact
    template_name = 'properties/contact_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Mensajes de Clientes'
        context['sidebar_subtitle'] = 'Revisar mensajes de consultas realizadas por potenciales clientes!'
        return context


# partials
class TableContactView(LoginRequiredMixin, View):
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
            'property': property_especific,
            'success': {'Mensaje enviado correctamente'}
        }
        html = render_block_to_string('properties/publication_detail.html', 'contact_detail', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'modal-contact-button'
        return response
    context = {
        'property': property_especific,
        'form': form,
        # 'errors': form.errors
    }
    html = render_block_to_string('properties/publication_detail.html', 'contact_detail', context)
    return HttpResponse(html)


# ========== CRUD PROPIEDADES PUBLICADAS EN VENTA ========== |

class PublishBuyListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'properties/publication_list.html'
    queryset = Publication.objects.filter(
        status=Publication.Status.PUBLISH,
        state=True,
        property__publish_type='ve'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_operation_buy'] = OperationBuyHistoryForm()
        context['publish_type'] = 've'
        context['sidebar_title'] = 'Publicaciones en Venta'
        context['sidebar_subtitle'] = 'Maneja la información de tus ventas!'
        return context


# ========== CRUD PROPIEDADES PUBLICADAS EN PERMUTA ========== |

class PublishExchangeListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'properties/publication_list.html'
    queryset = Publication.objects.filter(
        status=Publication.Status.PUBLISH,
        state=True,
        property__publish_type='pe'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publish_type'] = 'pe'
        context['sidebar_title'] = 'Publicaciones en Permuta'
        context['sidebar_subtitle'] = 'Maneja la información de tus permutas!'
        return context


# ========== CRUD PROPIEDADES PUBLICADAS EN ARRIENDO ========== |

class PublishRentListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'properties/publication_list.html'
    queryset = Publication.objects.filter(
        status=Publication.Status.PUBLISH,
        state=True,
        property__publish_type='ar'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publish_type'] = 'ar'
        context['sidebar_title'] = 'Publicaciones en Arriendo'
        context['sidebar_subtitle'] = 'Maneja la información de tus arriendos!'
        return context


# ========== CRUD PROPIEDADES PUBLICADAS EN ARRIENDO TEMPORADA ========== |

class PublishRentSeasonListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'properties/publication_list.html'
    queryset = Publication.objects.filter(
        status=Publication.Status.PUBLISH,
        state=True,
        property__publish_type='at'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publish_type'] = 'at'
        context['sidebar_title'] = 'Publicaciones en Arriendo de Temporada'
        context['sidebar_subtitle'] = 'Maneja la información de tus arriendos de temporada!'
        return context


# ========== CRUD PUBLICACIONES ========== |
@method_decorator(never_cache, name='dispatch')
class PublicationDetailView(View):
    def dispatch(self, request, pk, *args, **kwargs):
        publication = get_object_or_404(Publication, pk=pk)
        # Evita ver publicacion eliminada(state=False)
        if not publication.state or publication.status == 'dr':
            return redirect('reports:dashboard')
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk):
        form = PropertyContactForm(request.POST or None)  # no se puede asignar valor  de inicio a un elemento excluido
        message = None

        ip = get_ip(request)
        ip_visitor, _ = IpVisitor.objects.get_or_create(ip=ip)
        publication = get_object_or_404(Publication, id=pk)
        publication.views.add(ip_visitor)  # no es necesario comprobar nada, como es un manytomany, no se puede agregar la misma instancia 2 veces

        if publication.property.property_type == 'ca':
            property_especific = get_object_or_404(House, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.houses.first().num_rooms} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif publication.property.property_type == 'de':
            property_especific = get_object_or_404(Apartment, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.apartments.first().num_rooms} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif publication.property.property_type == 'of':
            property_especific = get_object_or_404(Office, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.offices.first().num_offices} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
        
        elif publication.property.property_type == 'su':
            property_especific = get_object_or_404(UrbanSite, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.urban_sites.first().num_lot} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
            
        elif publication.property.property_type == 'pa':
            property_especific = get_object_or_404(Parcel, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.parcels.first().num_lot} Lotes En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif publication.property.property_type == 'bo':
            property_especific = get_object_or_404(Cellar, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.cellars.first().num_local} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif publication.property.property_type == 'in':
            property_especific = get_object_or_404(Industrial, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.industrials.first().num_local} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif publication.property.property_type == 'lc':
            property_especific = get_object_or_404(Shop, property=publication.property)
            message = f'Hola , Estoy interesado en {publication.property.get_property_type_display()} en {publication.property.get_publish_type_display()} de {publication.property.shops.first().num_local} Dormitorios En {publication.property.commune.name}, por favor comunícate conmigo. ¡Gracias!'
    
        form.initial['message'] = message

        context = {
            'property': property_especific,
            'property_image': publication.property.property_images.all(),
            'form': form,
            'wa_message': publication.property.title,
            'wa_number': '56950092733',
            'publication': publication
        }
        return render(request, 'properties/publication_detail.html', context)


@method_decorator(never_cache, name='dispatch')
class PublicationCreateView(LoginRequiredMixin, View):
    def dispatch(self, request, uuid, slug, *args, **kwargs):
        property = Property.objects.filter(uuid=uuid, slug=slug).first()
        if not property.is_active:
            return redirect('reports:dashboard')
        if property.has_active_publication:
            return redirect('reports:dashboard')
        return super().dispatch(request, uuid, slug, *args, **kwargs)

    def get(self, request, uuid, slug, *args, **kwargs):
        property = Property.objects.filter(uuid=uuid, slug=slug).first()
        if property.publish_type == 'ar' or property.publish_type == 'at':
            form = PublicationRentForm(
                user=request.user, publish_type=property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        else:
            form = PublicationForm(
                user=request.user, publish_type=property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        context = {
            "form": form,
            'form_realtor': RealtorForm(),
            'form_owner': OwnerForm(),
            'title': 'Creación de Publicación',
            'subtitle': 'Maneje la creación de sus publicaciones',
        }
        return render(request, 'properties/publication_form.html', context)
    
    def post(self, request, uuid, slug, *args, **kwargs):
        property = Property.objects.filter(uuid=uuid, slug=slug).first()
        if property.publish_type == 'ar' or property.publish_type == 'at':
            form = PublicationRentForm(
                request.POST,
                user=request.user, publish_type=property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        else:
            form = PublicationForm(
                request.POST,
                user=request.user, publish_type=property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola

        # Valida si se puede publicar
        if property.has_active_publication:
            print('La propiedad tiene un publicacion en uso')
            messages.add_message(request, messages.INFO, "La propiedad tiene un publicacion en uso.")
        else:
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.property = property
                instance.save()
                return redirect('reports:dashboard')
            else:
                print(form.errors)
        context = {
            "form": form,
            'title': 'Creación de Publicación',
            'subtitle': 'Maneje la creación de sus publicaciones',
        }
        return render(request, 'properties/publication_form.html', context)  


@method_decorator(never_cache, name='dispatch')
class PublicationUpdateView(LoginRequiredMixin, View):
    def dispatch(self, request, pk, *args, **kwargs):
        publication = get_object_or_404(Publication, pk=pk)
        # Evita editar publicacion eliminada(state=False)
        if not publication.state:
            return redirect('reports:dashboard')
        return super().dispatch(request, pk, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        publication = get_object_or_404(Publication, pk=pk)
        if publication.property.publish_type == 'ar' or publication.property.publish_type == 'at':
            form = PublicationRentForm(
                instance=publication,
                user=request.user, publish_type=publication.property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        else:
            form = PublicationForm(
                instance=publication,
                user=request.user, publish_type=publication.property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        context = {
            "form": form,
            'title': 'Modificación de Publicación',
            'subtitle': 'Maneje la modificación de sus publicaciones'
        }
        return render(request, 'properties/publication_form.html', context)
 
    def post(self, request, pk, *args, **kwargs):
        publication = get_object_or_404(Publication, pk=pk)
        if publication.property.publish_type == 'ar' or publication.property.publish_type == 'at':
            form = PublicationRentForm(
                request.POST, instance=publication,
                user=request.user, publish_type=publication.property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        else:
            form = PublicationForm(
                request.POST, instance=publication,
                user=request.user, publish_type=publication.property.publish_type
            )  # forma mas robusta pasandosela al form y ahi asignandola
        if form.is_valid():
            form.save()
            return redirect('reports:dashboard')
        context = {
            "form": form,
            'title': 'Modificación de Publicación',
            'subtitle': 'Maneje la modificación de sus publicaciones'
        }
        return render(request, 'properties/publication_form.html', context) 


class PublicationDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        type_publish = request.GET.get('type_publish')
        page_number = request.GET.get('page_number', 1)

        publication = Publication.objects.get(id=kwargs['pk'])

        publication.state = False
        publication.save()
        # messages.success(request, "Propiedad eliminada correctamente")
        publication_list = Publication.objects.filter(
            status=Publication.Status.PUBLISH, state=True
        )
        if type_publish == 've':
            publication_list = publication_list.filter(
                property__publish_type='ve'
            )
            context['form_operation_buy'] = OperationBuyHistoryForm()
        if type_publish == 'pe':
            publication_list = publication_list.filter(
                property__publish_type='pe'
            )
            # context['form_operation_exchange'] = OperationExchangeHistoryForm()
        if type_publish == 'ar':
            publication_list = publication_list.filter(
                property__publish_type='ar'
            )
            # context['form_operation_rent'] = OperationRentHistoryForm()
        if type_publish == 'at':
            publication_list = publication_list.filter(
                property__publish_type='at'
            )
            # context['form_operation_rental_season'] = OperationRentalSeasonHistoryForm()

        paginator = Paginator(publication_list, 2)
        data = paginator.get_page(page_number)
        context['page_obj'] = data
        context['publish_type'] = type_publish
        
        html = render_block_to_string('properties/publication_list.html', 'table_list', context)
        return HttpResponse(html)


class PublicationChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        type_publish = request.GET.get('type_publish')
        page_number = request.GET.get('page_number', 1)
        action = request.GET.get('action')

        publication = get_object_or_404(Publication, id=kwargs['pk'])

        # Evita cambiar estado publicacion eliminada(state=False)
        if not publication.state:
            print('No puede cambiar estado de una publicacion eliminada')
        else:
            if action == 'normal':
                publication.is_featured = False
                publication.save()
                context['success'] = {'Publicación Normalizada Correctamente'}
            if action == 'featured':
                publication.is_featured = True
                publication.save()
                context['success'] = {'Publicación Destacada Correctamente'}
            if action == 'draft':
                publication.status = Publication.Status.DRAFT
                publication.save()
                context['success'] = {'Publicación Despublicada Correctamente'}
            if action == 'publish':
                publication.status = Publication.Status.PUBLISH
                publication.save()
    
                property_list = Property.objects.filter(state=True)
                paginator = Paginator(property_list, 2)
                properties_data = paginator.get_page(page_number)
                context['page_obj'] = properties_data
                context['success'] = {'Publicación Publicada Correctamente'}
                html = render_block_to_string('properties/properties_list.html', 'table_list', context)
                return HttpResponse(html)

            if action == 'finished':
                publication.operation = Publication.Operations.FINISHED
                publication.save()

            if action == 'annulled':
                publication.operation = Publication.Operations.ANNULLED
                publication.save()


        publication_list = Publication.objects.filter(state=True, status=Publication.Status.PUBLISH)

        if type_publish == 've':
            publication_list = publication_list.filter(property__publish_type='ve')
            context['form_operation_buy'] = OperationBuyHistoryForm()
        if type_publish == 'pe':
            publication_list = publication_list.filter(property__publish_type='pe')
            # context['form_operation_exchange'] = OperationExchangeHistoryForm()
        if type_publish == 'ar':
            publication_list = publication_list.filter(property__publish_type='ar')
            # context['form_operation_rent'] = OperationRentHistoryForm()
        if type_publish == 'at':
            publication_list = publication_list.filter(property__publish_type='at')
            # context['form_operation_rental_season'] = OperationRentalSeasonHistoryForm()
        if type_publish == 'random':
            property_list = Property.objects.filter(state=True)
            paginator = Paginator(property_list, 2)
            properties_data = paginator.get_page(page_number)
            context['page_obj'] = properties_data
            context['errors'] = {'Acción no Valida'}
            html = render_block_to_string('properties/properties_list.html', 'table_list', context)
            return HttpResponse(html)
          

        paginator = Paginator(publication_list, 2)
        publications_data = paginator.get_page(page_number)
        context['page_obj'] = publications_data
        context['publish_type'] = type_publish
        html = render_block_to_string('properties/publication_list.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TablePublicationView(LoginRequiredMixin, View):  # probe como pasar template y context con httpresponse en vez de render
    def get(sefl, request, *args, **kwargs):
        context = {}
        q = request.GET.get('q', '')
        type_publish = request.GET.get('type_publish')
        page_number = request.GET.get('page_number', 1)

        publication_list = Publication.objects.filter(
            property__commune_id__name__icontains=q,
            status=Publication.Status.PUBLISH, state=True
        )

        if type_publish == 've':
            publication_list = publication_list.filter(
                property__publish_type='ve'
            )
            context['form_operation_buy'] = OperationBuyHistoryForm()
        if type_publish == 'pe':
            publication_list = publication_list.filter(
                property__publish_type='pe'
            )
            # context['form_operation_exchange'] = OperationExchangeHistoryForm()
        if type_publish == 'ar':
            publication_list = publication_list.filter(
                property__publish_type='ar'
            )
            # context['form_operation_rent'] = OperationRentHistoryForm()
        if type_publish == 'at':
            publication_list = publication_list.filter(
                property__publish_type='at'
            )
            # context['form_operation_rental_season'] = OperationRentalSeasonHistoryForm()

        paginator = Paginator(publication_list, 2)
        publications_data = paginator.get_page(page_number)
        # template = get_template('properties/partials/property_table.html')
        context['page_obj'] = publications_data
        context['q'] = q
        context['publish_type'] = type_publish
        html = render_block_to_string('properties/publication_list.html', 'table_list', context)
        return HttpResponse(html)
        # return HttpResponse(template.render(context), content_type='html')


# =========== GENERAL PROPIEDADES ========== |

class PropertyListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'properties/properties_list.html'
    queryset = Property.objects.filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_option'] = 'table_property'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades!'
        return context


class PropertyDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page_number', 1)
        property = get_object_or_404(Property, uuid=kwargs['uuid'])
        property.state = False
        property.save()

        publication = Publication.objects.filter(property=property, state=True).first()
        if publication:
            publication.state = False
            publication.save()

        property_list = Property.objects.filter(state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data,
        }
        html = render_block_to_string('properties/properties_list.html', 'table_list', context)
        return HttpResponse(html)


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

    property_type_display = None
    if property_type == 'ca':
        form_extra = HouseForm(request.POST or None)
        property_type_display = 'Casa'
    elif property_type == 'de':
        form_extra = ApartmentForm(request.POST or None)
        property_type_display = 'Departemento'
    elif property_type == 'of':
        form_extra = OfficeForm(request.POST or None)
        property_type_display = 'Oficina'
    elif property_type == 'su':
        form_extra = UrbanSiteForm(request.POST or None)
        property_type_display = 'Sitio Urbano'
    elif property_type == 'pa':
        form_extra = ParcelForm(request.POST or None)
        property_type_display = 'Parcela'
    elif property_type == 'bo':
        form_extra = CellarForm(request.POST or None)
        property_type_display = 'Bodega'
    elif property_type == 'in':
        form_extra = IndustrialForm(request.POST or None)
        property_type_display = 'Industrial'
    elif property_type == 'lc':
        form_extra = ShopForm(request.POST or None)
        property_type_display = 'Local Comercial'
    else:
        return redirect('properties:property_custom_list')

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

        'title': f'Creación de Propiedad tipo {property_type_display}',
        'subtitle': 'Maneje la creación de sus propiedades',
        
        'property_type': property_type
    }
    return render(request, 'properties/property_form.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def property_update(request, slug, uuid):
    property = get_object_or_404(Property, uuid=uuid, slug=slug)
    # property = Property.objects.get(uuid=uuid, slug=slug)

    if property.publish_type == 'ar' or property.publish_type == 'at':
        form = PropertyRentForm(
            request.POST or None, request.FILES or None,
            publish_type=property.publish_type,
            instance=property
        )  # forma mas robusta pasandosela al form y ahi asignandola
    else:
        form = PropertyForm(
            request.POST or None, request.FILES or None,
            publish_type=property.publish_type,
            instance=property
        )  # forma mas robusta pasandosela al form y ahi asignandola

    communes = Commune.objects.all()

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
    else:
        communes = communes.filter(region=property.region)

    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
    else:
        commune = property.commune

    property_type_display = None

    if property.property_type == 'ca':
        house = House.objects.get(property=property)
        form_extra = HouseForm(request.POST or None, instance=house)
        property_type_display = 'Casa'
    elif property.property_type == 'de':
        apartment = Apartment.objects.get(property=property.id)
        form_extra = ApartmentForm(request.POST or None, instance=apartment)
        property_type_display = 'Departemento'
    elif property.property_type == 'of':
        office = Office.objects.get(property=property.id)
        form_extra = OfficeForm(request.POST or None, instance=office)
        property_type_display = 'Oficina'
    elif property.property_type == 'su':
        urban_site = UrbanSite.objects.get(property=property.id)
        form_extra = UrbanSiteForm(request.POST or None, instance=urban_site)
        property_type_display = 'Sitio Urbano'
    elif property.property_type == 'pa':
        parcel = Parcel.objects.get(property=property.id)
        form_extra = ParcelForm(request.POST or None, instance=parcel)
        property_type_display = 'Parcela'
    elif property.property_type == 'bo':
        cellar = Cellar.objects.get(property=property.id)
        form_extra = CellarForm(request.POST or None, instance=cellar)
        property_type_display = 'Bodega'
    elif property.property_type == 'in':
        industrial = Industrial.objects.get(property=property.id)
        form_extra = IndustrialForm(request.POST or None, instance=industrial)
        property_type_display = 'Industrial'
    elif property.property_type == 'lc':
        shop = Shop.objects.get(property=property.id)
        form_extra = ShopForm(request.POST or None, instance=shop)
        property_type_display = 'Local Comercial'
    else:
        return redirect('properties:property_custom_list')

    try:
        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic():  # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
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

        'title': f'Modificación de Propiedad tipo {property_type_display}',
        'subtitle': 'Maneje la modificación de sus propiedades',

        'property_type': property.property_type
    }
    return render(request, 'properties/property_form.html', context)


class PropertyGaleryView(LoginRequiredMixin, View):

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


class PropertySuccessDetailView(LoginRequiredMixin, DetailView):
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


# partials list
class PropertyIsActiveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')
        page_number = request.GET.get('page_number', 1)

        property = get_object_or_404(Property, id=kwargs['pk'])

        if property.has_active_publication:
            print('No puede cambiar estado de propiedad porque hay un publicacion vigente')
        else:
            if action == 'no_active':
                property.is_active = False
                property.save()

            if action == 'active':
                property.is_active = True
                property.save()

        property_list = Property.objects.filter(state=True)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data,
            'url_option': 'table_property'
        }
        html = render_block_to_string('properties/properties_list.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TablePropertyView(LoginRequiredMixin, View):
    def get(sefl, request, *args, **kwargs):

        q = request.GET.get('q', '')
        page_number = request.GET.get('page_number', 1)
        
        property_list = Property.objects.filter(
            commune_id__name__icontains=q,
            state=True
        )
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data, 
            'q': q,
        }
        html = render_block_to_string('properties/properties_list.html', 'table_list', context)
        return HttpResponse(html)


# partials create/update
@login_required
def property_select(request):
    return render(request, 'properties/property_select.html')


@login_required
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


@login_required
def realtor_create(request):
    form = RealtorForm(request.POST or None)
    context = {
        'form_realtor': form,
    }
    if form.is_valid():
        form.save()
        context['form_realtor'] = RealtorForm()
        context['success'] = {'Guardado correctamente'}
        html = render_block_to_string('properties/publication_form.html', 'realtor', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'realtor_select'
        return response
        
    html = render_block_to_string('properties/publication_form.html', 'realtor', context)
    return HttpResponse(html)


@login_required
def realtor_select(request):
    realtors = Realtor.objects.last()
    form = PublicationForm(initial={'realtor': realtors.id})

    context = {
        'form': form,
    }
    html = render_block_to_string('properties/publication_form.html', 'realtors', context)
    return HttpResponse(html)


@login_required
def owner_create(request):
    form = OwnerForm(request.POST or None)
    context = {
        'form_owner': form,
    }
    if form.is_valid():
        form.save()
        context['form_owner'] = OwnerForm()
        context['success'] = {'Guardado correctamente'}
        html = render_block_to_string('properties/publication_form.html', 'owner', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'owner_select'
        return response
        
    html = render_block_to_string('properties/publication_form.html', 'owner', context)
    return HttpResponse(html)


@login_required
def owner_select(request):
    owners = Owner.objects.last()
    form = PublicationForm(initial={'owner': owners.id})

    context = {
        'form': form,
    }
    html = render_block_to_string('properties/publication_form.html', 'owners', context)
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


