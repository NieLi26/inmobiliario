import os
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.core.files.storage import FileSystemStorage

from .utils import send_property_email
from .models import (
    PropertyContact, Property,
    PropertyImage, Publication
)
from apps.reports.models import OperationHistory

def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_property_email(instance.property.get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)
        

post_save.connect(contact_post_save, PropertyContact)


# def property_post_save(sender, instance, created, **kwargs):
#     if instance.status != 'pu' and instance.status != 'dr':

#         iva = ''
#         if instance.is_iva:
#             iva = 'con IVA'
#         else:
#             iva = 'sin IVA'

#         OperationHistory.objects.create(
#             type_property=f'{instance.get_property_type_display()} {instance.get_publish_type_display()}',
#             total='{0} {1} {2}'.format(instance.price, instance.get_type_price_display(), iva),
#             commission_percentage=instance.commission_percentage,
#             commission_value=instance.commission_value
#         )


# post_save.connect(property_post_save, Property)


# def property_pre_delete(sender, instance, **kwargs):
#     property_images = instance.property_images.all()
#     print(property_images)
#     while property_images.exists():
#         # get last images
#         property_image = property_images.last()
#         image = property_image.image.path
#         print(image)
        
#         # delete image
#         fs = FileSystemStorage()
#         fs.delete(image)

#         # delete instance
#         property_image.delete()


# pre_delete.connect(property_pre_delete, Property)


def property_images_pre_delete(sender, instance, **kwargs):
    image = instance.image.path

    # Check if the image exists
    if os.path.exists(image):
        # delete image
        fs = FileSystemStorage()
        fs.delete(image)
    else:
        print('Imagen no existe')


pre_delete.connect(property_images_pre_delete, PropertyImage)


def publication_pre_save(sender, instance, **kwargs):

    try:
        old_instance = Publication.objects.get(id=instance.pk)
        # se corrobora si operacion no es "En espera" y es una publicacion activa
        if not instance.operation == "wa" and old_instance.state:

            iva = ''
            if instance.is_iva:
                iva = 'con IVA'
            else:
                iva = 'sin IVA'

            OperationHistory.objects.create(
                type_property=f'{instance.property.get_property_type_display()} {instance.property.get_publish_type_display()}',
                operation=instance.get_operation_display(),
                codigo=instance.property.uuid,
                region=instance.property.region,
                commune=instance.property.commune,
                total='{0} {1} {2}'.format(instance.price, instance.get_type_price_display(), iva),
                commission_percentage=instance.commission_percentage if instance.commission_percentage else 0,
                commission_value=instance.commission_value
            )
            instance.state = False

    except Publication.DoesNotExist:
        pass


pre_save.connect(publication_pre_save, Publication)


def publication_post_save(sender, instance, created, **kwargs):
    # desactivamos propiedad al crear publicacion
    if created:
        property = instance.property
        property.is_active = False
        property.save()


post_save.connect(publication_post_save, Publication)


# def operation_history_post_save(sender, instance, created, **kwargs):
#     # desactivamos propiedad al crear publicacion
#     if created:
#         publication = Publication.objects.get(property__uuid=instance.codigo)
#         publication.state = False
#         publication.save()


# post_save.connect(operation_history_post_save, OperationHistory)
