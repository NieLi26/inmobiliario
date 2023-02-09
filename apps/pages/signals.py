from django.db.models.signals import post_save

from .utils import send_general_email, send_owner_email
from .models import Contact, OwnerContact


def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_general_email(instance.name, instance.phone, instance.subject, instance.message, instance.from_email)
        
post_save.connect(contact_post_save, Contact)

def contact_owner_post_save(sender, instance, created, **kwargs):
    if created:
        send_owner_email(instance.name, instance.phone, instance.subject, instance.message, instance.from_email)
        
post_save.connect(contact_owner_post_save, OwnerContact)