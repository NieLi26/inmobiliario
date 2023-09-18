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

