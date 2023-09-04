import os
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Email
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template

from .models import Property, Commune


def delete_file(image):
    ''' Recibe una ruta '''
    # Check if the image exists
    if os.path.exists(image):
        # delete image
        fs = FileSystemStorage()
        fs.delete(image)
    else:
        print('Imagen no existe')


def get_ip(request):
    # obtener ip de cuando se aloja en servidor proxy
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        # obtenerlo cuando se aloja ne servidor local
        return request.META.get('REMOTE_ADDR')
    # devuelve la dirección IP de la máquina en la que se está ejecutando el código
    # hostname = socket.gethostname()
    # return socket.gethostbyname(hostname)


# def can_property(request, property_type=None):
#     ''' Deniega permiso a vista de creacion si se sobrepasa el limite de publicaciones que permite la subscripcion'''
#     list_property_type = [i[0] for i in Property.PROPERTY_CHOICES]
#     if property_type not in list_property_type:
#         raise Http404
#     elif not request.user.is_superuser:
#         if Property.count_by_user(request.user) >= request.user.subscription.pricing.allowed_property: # evita crear o editar si se pasa de las propiedades maximas
#             raise PermissionDenied
#     return request

# def can_edit_property(request, slug=None, uuid=None):
#     ''' Deniega permiso a vista de edicion sino es le usuario que la creo'''
#     property = Property.objects.filter(uuid=uuid, slug=slug).first()
#     if property is None:
#         # raise ObjectDoesNotExist("La propiedad no existe.")
#         raise Http404
#     if not request.user.is_superuser and property.user != request.user:
#         raise PermissionDenied
#     return request


# tipo publicacion - tipo propiedad - locacion
def url_custom_list(publish_type, property_type, location_slug, page_number=None): 
    list_property_type = [i[0] for i in Property.PROPERTY_CHOICES]
    list_location_slug = [i.location_slug for i in Commune.objects.all()]

    try:

        if (publish_type != 've' and publish_type != 'ar' and publish_type != 'at' and publish_type != 'pe' ) and property_type in list_property_type and location_slug in list_location_slug:
            print('entrre en propiedad - locacion')
            return reverse('properties:custom_list_publish_property', args=[property_type, location_slug])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe' ) and property_type not in list_property_type and location_slug in list_location_slug:
            print('entrre en publicacion - locacion')
            return reverse('properties:custom_list_publish_property', args=[publish_type, location_slug])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe' ) and location_slug not in list_location_slug and property_type in list_property_type:
            print('entrre en publicacion - propiedad')
            return reverse('properties:custom_list_publish_property', args=[publish_type, property_type])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe' ) and location_slug not in list_location_slug and property_type not in list_property_type:
            return redirect('properties:custom_list_publish', args=[publish_type])
        elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at' and publish_type != 'pe' ) and property_type not in list_property_type and location_slug in list_location_slug:
            return reverse('pages:home')
        elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at' and publish_type != 'pe' ) and property_type in list_property_type and location_slug not in list_location_slug:
            return reverse('pages:home')
            
    except ObjectDoesNotExist:
        return reverse('properties:custom_list_publish_property', args=[publish_type, property_type])
    
    return False


# tipo publicacion - tipo propiedad o tipo publicacion - locacion o tipo propiedad - locacion
def url_custom_list_publish_property(first_data, second_data):
    list_property_type = [i[0] for i in Property.PROPERTY_CHOICES]
    list_location_slug = [i.location_slug for i in Commune.objects.all()]
    properties = Property.objects.all()
    
    try:
        if (first_data != 've' and first_data != 'ar' and first_data != 'at' and first_data != 'pe' ) and first_data in list_property_type and second_data in list_location_slug:
            print('entrre en propiedad - locacion')
            qs = properties.filter(property_type=first_data, commune__location_slug=second_data)

            property_type = [display_value for value, display_value in Property.PROPERTY_CHOICES if value == first_data][0]
            location_slug = [i.name for i in Commune.objects.all() if second_data in i.location_slug][0]
            entity = '{0} en {1}'.format(property_type, location_slug)

            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at' or first_data == 'pe' )  and second_data not in list_property_type and second_data in list_location_slug:
            print('entrre en publicacion - locacion')
            qs = properties.filter(publish_type=first_data, commune__location_slug=second_data)

            location_slug = [i.name for i in Commune.objects.all() if second_data in i.location_slug][0]

            if first_data == 've':
                entity = f'Ventas en {location_slug}'
            elif first_data == 'ar':
                entity = f'Arriendos en {location_slug}'
            elif first_data == 'pe':
                entity = f'Permutas en {location_slug}'
            else:
                entity = f'Arriendos temporada en {location_slug}'
            
            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at' or first_data == 'pe' ) and second_data in list_property_type and second_data not in list_location_slug:
            print('entrre en publicacion - propiedad')
            qs = properties.filter(publish_type=first_data, property_type=second_data)

            property_type = [display_value for value, display_value in Property.PROPERTY_CHOICES if value == second_data][0]

            if first_data == 've':
                entity = f'Ventas de {property_type}'
            elif first_data == 'ar':
                entity = f'Arriendos de {property_type}'
            elif first_data == 'pe':
                entity = f'Permutas de {property_type}'
            else:
                entity = f'Arriendos temporada de {property_type}'

            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at' or first_data == 'pe' ) and second_data not in list_property_type and second_data not in list_location_slug:
            return reverse('properties:custom_list_publish', args=[first_data])

        else:
            # messages.error(request, 'Ha ocurrido un error inesperado')
            return reverse('pages:home')
    except Exception as e:
        print(str(e))
        return reverse('pages:home')


def send_property_email(property, name, phone, subject, message, from_email):
    try:
        # messages.success(request, "Mensaje enviado correctamente")    
        # return redirect('pages:contact_create')
        template = get_template('properties/contact_property.txt') # genera instancia del template
        context = {
            'name': name,
            'email': from_email,
            'phone': phone,
            'message': message,
            'link': f'http://127.0.0.1:8000{property}'
        }

        # cargamos el contexto dentro del template
        message = template.render(context)
        
        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['theprimatesfactoryinc@gmail.com']
        )
        
        # convert the html and css inside the "contact_form.txt" in html template
        email.content_subtype = 'html'
        email.send()

        return HttpResponse('Mensaje enviado correctamente')
    except BadHeaderError:
        return HttpResponse('Se ha encontrado un asunto no valido')
    except Exception as e:
        print(str(e))
        pass