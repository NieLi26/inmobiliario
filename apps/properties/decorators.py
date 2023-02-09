import functools
from . import utils
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Property, Commune

# based off the decorator template from the previous example


def url_custom_list_decorator(view_func):
    """Check if url is Correct"""
    # @functools.wraps(view_func) # no es necesario es por buena practica para el mantenimiento del proyecto
    def wrap(request, *args, **kwargs):
        response = utils.url_custom_list(*args, **kwargs)
        if response:
            return redirect(response)
        else:
            return view_func(request, *args, **kwargs)

    return wrap


# def check_properties(view_func):
#     """Check if a user can add properties"""
#     @functools.wraps(view_func)
#     def new_view_func(request, property_type):
#         # Act on the request object with utils.can_properties()
#         request = utils.can_property(request, property_type)
#         # Call the view function
#         response = view_func(request, property_type)
#         # Return the HttpResponse object
#         return response
#     return new_view_func


# def check_edit_properties(view_func):
#     """Check if a user can edit properties"""
#     @functools.wraps(view_func)
#     def new_view_func(request, slug, uuid):
#         # Act on the request object with utils.can_edit_property()
#         request = utils.can_edit_property(request, slug, uuid)
#         # Call the view function
#         response = view_func(request, slug, uuid)
#         # Return the HttpResponse object
#         return response
#     return new_view_func


############ FORMA DIRECTA SIN UTILS.PY ###############
# def url_custom_list_decorator(view_func):
#     """Check if url is Correct"""
#     @functools.wraps(view_func) # no es necesario es por buena practica para el mantenimiento del proyecto
#     def wrap(request, *args, **kwargs):
#         property_choices = Property.PROPERTY_CHOICES
#         list_property_type = [i[0] for i in property_choices]
#         list_location_slug = [i.location_slug for i in Commune.objects.all()]
#         publish_type = kwargs['publish_type']
#         property_type = kwargs['property_type']
#         location_slug = kwargs['location_slug']
#         try:

#             if (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type in list_property_type and location_slug in list_location_slug:
#                 print('entrre en propiedad - locacion')
#                 return redirect('properties:custom_list_publish_property', property_type, location_slug)
#             elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and property_type not in list_property_type and location_slug in list_location_slug:
#                 print('entrre en publicación - locacion')
#                 return redirect('properties:custom_list_publish_property', publish_type, location_slug)
#             elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and location_slug not in list_location_slug and property_type in list_property_type:
#                 print('entrre en publicación - propiedad')
#                 return redirect('properties:custom_list_publish_property', publish_type, property_type)
#             elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and location_slug not in list_location_slug and property_type not in list_property_type:
#                 return redirect('properties:custom_list_publish', publish_type)
#             elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type not in list_property_type and location_slug in list_location_slug:
#                 return redirect('home')
#             elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type in list_property_type and location_slug not in list_location_slug:
#                 return redirect('home')
            
#         except ObjectDoesNotExist:
#             return redirect('properties:custom_list_publish_property', publish_type, property_type)
#         else:
#             return view_func(request, *args, **kwargs)
#         # Return the HttpResponse object


#     return wrap