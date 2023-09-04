from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver

from .utils import send_property_email, delete_file
from .models import (
    PropertyContact, Property,
    PropertyImage, Publication
)
from apps.reports.models import OperationBuyHistory, OperationRent


def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_property_email(instance.property.publications.last().get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)


post_save.connect(contact_post_save, PropertyContact)


@receiver(pre_delete, sender=PropertyImage)
def property_images_pre_delete(sender, instance, **kwargs):
    image = instance.image.path
    delete_file(image)


@receiver(post_save, sender=Publication)
def publication_post_save(sender, instance, created, **kwargs):
    try:
        if instance.operation == "fi":
            if instance.property.publish_type == 've':
                OperationBuyHistory.objects.create(publication=instance)
            elif instance.property.publish_type == 'ar':
                OperationRent.objects.create(publication=instance)
    except Exception as e:
        print(str(e))
        pass

