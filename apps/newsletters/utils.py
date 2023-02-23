from django.http import HttpResponse
from django.conf import settings

# Email
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template


def send_newsletter_email(property, name, phone, subject, message, from_email):
    try:
        # messages.success(request, "Mensaje enviado correctamente")    
        # return redirect('pages:contact_create')
        template = get_template('properties/contact_property.txt')  # genera instancia del template
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