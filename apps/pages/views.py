import json
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, View

# cloudinary
import cloudinary

# for htmx
from render_block import render_block_to_string

# email
# from django.template import loader
# from django.core.mail import EmailMultiAlternatives

# cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from apps.newsletters.forms import NewsletterUserForm
from .forms import ContactForm, OwnerContactForm
from .models import Contact, OwnerContact
from apps.properties.models import (
    Commune, House, Apartment,
    Property, Publication
)



def custom_alert(message, tag):
    alert = []
    context = {
        'message': message,
        'tags': tag
    }
    alert.append(context)
    return alert


class TestTemplateView(TemplateView):
    template_name = 'test.html'

    # def get(self, request, *args, **kwargs):

    #     property_images = PropertyImage.objects.filter(property__id=1)
    #     for i in property_images:
    #         print(i.image)
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        imagen = request.FILES.get('imagen')

        if imagen:
            try:
                cloudinary.config( 
                    cloud_name=settings.CLOUD_NAME, 
                    api_key=settings.CLOUD_API_KEY, 
                    api_secret=settings.CLOUD_API_SECRET 
                )

                cloudinary.uploader.upload(imagen)
            except Exception as e:
                print(str(e))

        return render(request, 'test.html')

        # data = dict()
        # try:
        #     print(request.POST)
        #     print(request.FILES)
        #     action = json.loads(request.body)['action']
        #     if action == 'delete':
        #         imagen = json.loads(request.body)['imagen']
        #         property_image = PropertyImage.objects.get(image=imagen)
        #         property_image.delete()
        #     else:
        #         data['error'] = 'Ha ocurrido un error'
        # except Exception as e:
        #     print(str(e))
        #     data['error'] = str(e)
        # return JsonResponse(data)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     property = Property.objects.get(id=1)
    #     property_images = PropertyImage.objects.filter(property__id=1)
    #     context['property_images'] =  property_images
    #     context['property'] =  property
    #     return context


# ========== GENERAL ========== |

@method_decorator(never_cache, name='dispatch')
class HomePageView(View):
    def get(self, request, *args, **kwargs):
        # houses = House.objects.filter(
        #     property__state=True, property__publications__is_featured=True,
        #     property__publications__status=Publication.Status.PUBLISH
        # ).distinct()[0:20]

        # apartments = Apartment.objects.filter(
        #     property__state=True, property__publications__is_featured=True,
        #     property__publications__status=Publication.Status.PUBLISH
        # ).distinct()[0:20]

        publications = Publication.objects.filter(
            state=True, is_featured=True,
            status=Publication.Status.PUBLISH
        )

        publication_houses = publications.filter(property__property_type='ca') \
                                         .distinct()[0:20]

        publication_apartments = publications.filter(property__property_type='de') \
                                             .distinct()[0:20]

        form_newsletters = NewsletterUserForm()
        context = {
           'house_list': publication_houses,
           'apartment_list': publication_apartments,
           'form_newsletters': form_newsletters,
        }
        return render(request, 'pages/home.html', context)

    def post(self, request, *args, **kwargs):
        houses = House.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]
        apartments = Apartment.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]

        publish_type = request.POST.get('q_publish', '')
        property_type = request.POST.get('q_property', '')
        search_location = request.POST.get('search_location', '')

        if publish_type != '' and property_type != '':
            if search_location != '':
                communes = Commune.objects.all()
                location_slug = [commune for commune in communes if commune.get_commune_region() == search_location]
          
                if location_slug:
                    location_slug = location_slug[0]
                    location_slug= location_slug.location_slug
                else:
                    
                    return redirect(reverse('properties:custom_list_publish_property', kwargs={
                        'first_data':publish_type,
                        'second_data':property_type,
                    }))
                # location_slug = Property.objects.filter(commune=location_slug)[0]
                # try :
                # except:
                #     return redirect(reverse('custom_list_region_commune', args=[publish_type, property_type]))
                return redirect(reverse('properties:custom_list', kwargs={
                    'publish_type':publish_type,
                    'property_type':property_type,
                    'location_slug':location_slug
                }))
            else:
                return redirect(reverse('properties:custom_list_publish_property', kwargs={
                    'first_data':publish_type,
                    'second_data':property_type,
                }))

        context = {
           'house_list': houses,
           'apartment_list': apartments,
        }

        return render(request, 'pages/home.html', context)


# partials
def hx_side_alert(request):
    return render(request, 'components/custom_sidealert.html')


def hx_search_location(request):
    search_location = request.POST.get('search_location', '')
    communes = Commune.objects.all()
    results = [commune for commune in communes if search_location.lower() in commune.get_commune_region().lower()]

    context = {
        'results': results
    }
    html = render_block_to_string('pages/home.html', 'search_results', context)
    return HttpResponse(html)


# ========== CONTACT ========== |
@method_decorator(never_cache, name='dispatch')
class ContactPageView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        SUBJECTS = (
            ('', 'Seleccione una opción'),
        )
        subject = ''
        disabled = 'disabled'
        context = {
            'form': form,
            'subjects': SUBJECTS,
            'subject_selected': subject,
            'disabled': disabled,
        }
        return render(request, 'pages/contact_create.html', context)
   
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        SUBJECTS = (
            ('', 'Seleccione una opción'),
        )
        subject = request.POST.get('subject', '')
        disabled = 'disabled'
        category = request.POST.get('category')
        if category:
            if category == 'propietario':
                SUBJECTS = (
                    ('', 'Seleccione una opción'),
                    ('Quiero arrendar mi propiedad', 'Quiero arrendar mi propiedad'),
                    ('Quiero vender mi propiedad', 'Quiero vender mi propiedad'),
                )
                disabled = ''
            elif category == 'arrendatario':
                SUBJECTS = (
                    ('', 'Seleccione una opción'),
                    ('Quiero arrendar por temporada', 'Quiero arrendar por temporada'),
                    ('Quiero arrendar por año corrido', 'Quiero arrendar por año corrido'),
                )
                disabled = ''
            elif category == 'comprador':
                SUBJECTS = (
                    ('', 'Seleccione una opción'),
                    ('Quiero comprar una propiedad', 'Quiero comprar una propiedad'),
                    ('Quiero visitar una propiedad', 'Quiero visitar una propiedad'),
                    ('Necesito permutar un propiedad', 'Necesito permutar un propiedad'),
                )
                disabled = ''

        context = {
            'form': form,
            'subjects': SUBJECTS,
            'disabled': disabled,
            'subject_selected': subject,
        }

        if form.is_valid():
            form.save()
            context['form'] = ContactForm()
            context['disabled'] = 'disabled'
            context['subject_selected'] = ''
            context['success'] = {'Mensaje enviado correctamente'}
            html = render_block_to_string(
                'pages/contact_create.html',
                'contact_form', context
            )
            response = HttpResponse(html)
            response['HX-Trigger'] = 'modal-contact-button'
            return response
        context['errors'] = {'Mensaje no enviado'}
        # context['errors'] = form.errors.values()
        html = render_block_to_string(
            'pages/contact_create.html',
            'contact_form',
            context
        )
        return HttpResponse(html)


class ContactListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        contact_list = ContactForm.Meta.model.objects.all()
        paginator = Paginator(contact_list, 2)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
            'sidebar_title': 'Mensajes de Clientes',
            'sidebar_subtitle': 'Revisar mensajes de consultas realizadas por potenciales clientes!'
        }
        return render(request, 'pages/contact_list.html', context) 


# partials
def hx_subject_select(request):

    category = request.GET.get('category', '')
    print(category)
    SUBJECTS = (
            ('', 'Seleccione una opción'),
    )
    disabled = ''
    if category:
        if category == 'propietario':
            SUBJECTS = (
                ('', 'Seleccione una opción'),
                ('Quiero arrendar mi propiedad', 'Quiero arrendar mi propiedad'),
                ('Quiero vender mi propiedad', 'Quiero vender mi propiedad'),
            )
        elif category == 'arrendatario':
            SUBJECTS = (
                ('', 'Seleccione una opción'),
                ('Quiero arrendar por temporada', 'Quiero arrendar por temporada'),
                ('Quiero arrendar por año corrido', 'Quiero arrendar por año corrido'),
            )
        elif category == 'comprador':
            SUBJECTS = (
                ('', 'Seleccione una opción'),
                ('Quiero comprar una propiedad', 'Quiero comprar una propiedad'),
                ('Quiero visitar una propiedad', 'Quiero visitar una propiedad'),
                ('Necesito permutar un propiedad', 'Necesito permutar un propiedad'),
            )
    else:
        disabled = 'disabled'

    context = {
        'subjects': SUBJECTS,
        'disabled': disabled,
    }
    html = render_block_to_string('pages/contact_create.html', 'subject', context)
    return HttpResponse(html)


def hx_contact_home_form(request):
    form = OwnerContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        # messages.success(request, "Mensaje enviado correctamente")  
        msg = custom_alert('Mensage enviado correctamente', 'success')
        html = render_block_to_string('pages/home.html', 'contact_home_form', {'form': OwnerContactForm(), 'messages': msg})
        response = HttpResponse(html)
        response['HX-Trigger'] = 'modal-contact-button'
        return response

    html = render_block_to_string('pages/home.html', 'contact_home_form', {'form': form})
    return HttpResponse(html)


def hx_contact_table(request, page_number):
    q = request.GET.get('q', '')

    contact_list = Contact.objects.filter(name__icontains=q)
    
    paginator = Paginator(contact_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        # 'contact_list': properties_data,
        'page_obj': properties_data,
        'q': q
    }
    html = render_block_to_string('pages/contact_list.html', 'table_list', context)
    return HttpResponse(html)


def hx_contact_modal(request, pk, page_number):
    contact = Contact.objects.get(id=pk)
    contact.state = False
    contact.save()
    contact_list = ContactForm.Meta.model.objects.all()
    paginator = Paginator(contact_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data,
    }
    html = render_block_to_string(
        'pages/contact_list.html',
        'table_list',
        context
    )
    response = HttpResponse(html)
    # pasamos un encabezado para activar el trigger
    response['HX-Trigger'] = 'modal-contact-button'
    return response


def hx_contact_notify(request):
    qs = Contact.objects.filter(state=True)
    if qs.exists():
        contact_count = qs.count()
    else:
        contact_count = 0
    context = {
        'contact_count' : contact_count,
    }
    html = render_block_to_string('navigation/_navbar.html', 'contact_notify', context)
    return HttpResponse(html)


def hx_tostify_alert(request):
    html = render_block_to_string('base.html', 'toastify_alert')
    return HttpResponse(html)
