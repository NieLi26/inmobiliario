import socket
import json
from django.shortcuts import render, redirect
# from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, View


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
        data = dict()
        try:
            print(request.POST)
            print(request.FILES)
            action = json.loads(request.body)['action']
            if action == 'delete':
                imagen = json.loads(request.body)['imagen']
                property_image = PropertyImage.objects.get(image=imagen)
                property_image.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data)

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
        houses = House.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]

        apartments = Apartment.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]

        form = OwnerContactForm()
        form_newsletters = NewsletterUserForm()
        context = {
           'house_list': houses,
           'apartment_list': apartments,
           'form': form,
           'form_newsletters': form_newsletters,
        }
        return render(request, 'pages/home.html', context)

    def post(self, request, *args, **kwargs):
        form = OwnerContactForm(request.POST)

        houses = House.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]
        apartments = Apartment.objects.filter(
            property__state=True, property__publications__is_featured=True,
            property__publications__status=Publication.Status.PUBLISH).distinct()[0:20]

        publish_type = request.POST.get('q_publish', '')
        property_type = request.POST.get('q_property', '')
        search_location = request.POST.get('search_location', '')

        if publish_type != '' and property_type !='':
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

        # context['errors'] = form.errors.values()
        html = render_block_to_string(
            'pages/contact_create.html',
            'contact_form',
            context
        )
        return HttpResponse(html)


class ContactListView(View):
    def get(self, request, *args, **kwargs):
        contact_list = ContactForm.Meta.model.objects.all()
        paginator = Paginator(contact_list, 2)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
            'sidebar_title': 'Contactos',
            'sidebar_subtitle': 'Maneja la información de contactos generales!'
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
    # return render(request, 'components/contact_notify.html')


# ========== OWNER CONTACT ========== |
class OwnerContactListView(ListView):
    model = OwnerContact
    template_name = 'pages/contact_owner_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Contactos'
        context['sidebar_subtitle'] = 'Maneja la información de contactos de propietarios!'
        return context


# partials
class TableOwnerContactView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')

        contact_list = OwnerContact.objects.filter(name__icontains=q)

        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
            'q': q
        }
        html = render_block_to_string('pages/contact_owner_list.html', 'table_contact_owner', context)
        return HttpResponse(html)


class ModalOwnerContactView(View):
    def get(self, request, *args, **kwargs):
        contact = OwnerContact.objects.get(id=kwargs['pk'])
        contact.state = False
        contact.save()
        contact_list = OwnerContact.objects.all()
        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data,
        }
        html = render_block_to_string('pages/contact_owner_list.html', 'table_contact_owner', context)
        return HttpResponse(html)


# def hx_message(request):
#     return render(request, 'partials/contact_alerts.html')


# class ContactPageView(FormView):
#     template_name = 'pages/contact.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('contact')

#     def form_valid(self, form):
#         subject = form.cleaned_data['subject']
#         # name = form.cleaned_data['name']
#         # phone = form.cleaned_data['phone']
#         from_email = form.cleaned_data['from_email']
#         message = form.cleaned_data['message']
#         try:
#             send_mail(subject, message, from_email, ['seba.diamond5@gmail.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return super().form_valid(form)

    

# def contactView(request):
#     if request.method == 'GET':
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(subject, message, from_email, ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, "email.html", {'form': form})

# def successView(request):
#     return HttpResponse('Success! Thank you for your message.')


####################### mensaje en signals ##########################
# class ContactPageView(SuccessMessageMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = ContactForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'pages/contact.html', context)
    
#     def post(self, request, *args, **kwargs):
#         form = ContactForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = 'Su correo ha sido recibido satisfactoriamente lo contactaremos a la brevedad'
#             try:
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_email])
#                 messages.success(request, "Mensaje enviado correctamente")    
#                 return redirect('contact')
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#         return render(request, 'pages/contact.html', {'form': form})