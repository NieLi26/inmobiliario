from email import message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
# from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages

# for gmail
from django.template.loader import get_template

#cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .models import NewsletterUser
from .forms import NewsletterUserForm

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class NewsletterUserView(View):
    
    def post(self, request, *args, **kwargs):
        form = NewsletterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Su correo ha sido agregado')
        else:
            print(form.errors['email'])
            messages.error(request, form.errors['email'])
        #     name = instance.name
        #     subject = instance.subject
        #     from_email = instance.from_email
        #     phone = instance.phone
        #     message = instance.message
        #     try:
        #         template = get_template('pages/contact_form.txt') # genera instancia del texto
        #         context = {
        #             'name': name,
        #             'email': from_email,
        #             'phone': phone,
        #             'message': message,
        #         }
        #         # message = template.render(context)
        #         email = EmailMultiAlternatives(
        #             subject,
        #             message,
        #             settings.DEFAULT_FROM_EMAIL,
        #             ['seba.diamond5@gmail.com']
        #         )
                
        #         # convert the html and css inside the "contact_form.txt" in html template
        #         email.content_subtype = 'html'
        #         email.send()

        #         messages.success(request, "Mensaje enviado correctamente")    
        #         return redirect('contact')
        #     except Exception as e:
        #         print(str(e))      
        return HttpResponseRedirect(reverse_lazy('pages:home'))