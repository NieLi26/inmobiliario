from secrets import choice
from django.db import models

from apps.base.models import TimeStampedModel
# Create your models here.


class Contact(TimeStampedModel):
    """Model definition for Contact."""

    # class Subjects(models.TextChoices):
    #     EMPTY = '', 'Seleccione una opción'
    #     ASUNTO_1 = 'a1', 'Asesoría Legal'
    #     ASUNTO_2 = 'a2', 'Tasación de Bienes Raíces Urbanos y Rurales'
    #     ASUNTO_3 = 'a3', 'Estudios de titulo'
    #     ASUNTO_4 = 'a4', 'Escrituras de Promesa Compraventa'

    class Categorys(models.TextChoices):
        EMPTY = '', 'Seleccione una opción'
        OWNER = 'propietario', 'Propietario'
        BUYER = 'comprador', 'Comprador'
        TENANT = 'arrendatario', 'Arrendatario'

    # TODO: Define fields here
    name = models.CharField('Nombre', max_length=200)
    from_email = models.EmailField('Email', max_length=50)
    category = models.CharField('Categoria', choices=Categorys.choices, max_length=15)
    subject = models.CharField('Asunto', max_length=50)
    phone = models.CharField('Télefono(opcional)', max_length=9, blank=True)
    message = models.TextField('Mensaje')

    class Meta:
        """Meta definition for Contact."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return self.name


class OwnerContact(TimeStampedModel):

    class Subjects(models.TextChoices):
        ASUNTO_0 = '', 'Seleccione un tipo'
        ASUNTO_1 = 'Venta', 'Venta'
        ASUNTO_2 = 'Arriendo', 'Arriendo'
        ASUNTO_3 = 'Arriendo Temporada', 'Arriendo Temporada'
        ASUNTO_4 = 'Permuta', 'Permuta'

    '''Model definition for OwnerContact.'''
    name = models.CharField('Nombre Completo', max_length=200)
    from_email = models.EmailField('Email', max_length=50)
    subject = models.CharField('Asunto', choices=Subjects.choices, max_length=50)
    phone = models.CharField('Télefono(opcional)', max_length=9, blank=True)
    message = models.TextField('Mensaje')
    
    class Meta:
        '''Meta definition for OwnerContact.'''

        verbose_name = 'OwnerContact'
        verbose_name_plural = 'OwnerContacts'

    def __str__(self):
        return str(self.from_email)