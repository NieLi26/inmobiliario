from django.shortcuts import redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            # if request.headers.get("HX-Request") == "true":
            if request.htmx:
                # return HttpResponseClientRefresh()
                return HttpResponseClientRedirect(reverse_lazy("reports:dashboard"))
            return redirect("reports:dashboard")
        return super().dispatch(request, *args, **kwargs) 


class PaginationMixin:
    paginate_by = 2
