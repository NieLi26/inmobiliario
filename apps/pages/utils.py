from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.template.loader import get_template

# send_mail
# def send_general_email(subject, message, from_email):
#     """ Ejemplo con para solo texto fijo"""
#     try:
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['theprimatesfactoryinc@gmail.com'])
#         # messages.success(request, "Mensaje enviado correctamente")    
#         # return redirect('pages:contact_create')
#         return HttpResponse('Mensaje enviado correctamente')
#     except BadHeaderError:
#         return HttpResponse('Se ha encontrado un asunto no valido')
#     except Exception as e:
#         print(str(e))
#         pass

# EmailMultiAlternatives
def send_general_email(name, phone, subject, message, from_email):
    """ Ejemplo con para adjuntar contexto, html,css, archivo adjunto y multiples correos"""
    try:
        template = get_template('pages/contact_general.txt') # genera instancia del template
        context = {
            'name': name,
            'email': from_email,
            'phone': phone,
            'message': message,
            'link': 'https://sistemagestion.propiedadesweb.cl/'
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

def send_owner_email(name, phone, subject, message, from_email):
    print('ENTRE')
    try:
        template = get_template('pages/contact_owner.txt') # genera instancia del template
        context = {
            'name': name,
            'email': from_email,
            'phone': phone,
            'message': message,
            'link': 'https://sistemagestion.propiedadesweb.cl/'
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

        # messages.success(request, "Mensaje enviado correctamente")    
        return HttpResponse('Mensaje enviado correctamente')
    except BadHeaderError:
        return HttpResponse('Se ha encontrado un asunto no valido')
    except Exception as e:
        print(str(e))
        pass
