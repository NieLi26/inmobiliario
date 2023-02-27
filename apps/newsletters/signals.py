from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .utils import send_newsletter_email
from apps.properties.models import Property


# @receiver(post_save, sender=Property)
# def send_newsletter_post_save(sender, instance,  **kwargs):
#     # instance = kwargs['instance']
#     # print('ante de obtener instancia')
#     # print(instance)
#     if instance.status == 'pu':
#         if instance.properties.first():
#             print(instance.properties.first().image.path)
#         # else:
#         #     pass
#         print(settings.STATIC_ROOT)
#         print(settings.STATIC_URL)
#         print(settings.MEDIA_ROOT)
#         print(settings.MEDIA_URL)
#         print('SE PUBLICO SHIIII')
#         # send_newsletter_email(instance.property.get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)
 