import os
from django.db.models.signals import post_save, post_delete, pre_delete
from django.core.files.storage import FileSystemStorage

from .utils import send_property_email
from .models import (
    PropertyContact, PropertyManager, Property,
    PropertyImage
)


def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_property_email(instance.property.get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)
        

post_save.connect(contact_post_save, PropertyContact)


def property_post_save(sender, instance, created, **kwargs):
    if instance.status != 'pu' and instance.status != 'dr':

        iva = ''
        if instance.is_iva:
            iva = 'con IVA'
        else:
            iva = 'sin IVA'

        PropertyManager.objects.create(
            property=instance,
            type_property=f'{instance.get_property_type_display()} {instance.get_publish_type_display()}',
            total='{0} {1} {2}'.format(instance.price, instance.get_type_price_display(), iva),
            commission_percentage=instance.commission_percentage,
            commission_value=instance.commission_value
        )


post_save.connect(property_post_save, Property)


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
