from django.db import models
from apps.base.models import TimeStampedModel


# Create your models here.
class Client(TimeStampedModel):
    '''Model definition for Cliente.'''
    first_name = models.CharField('Nombre', max_length=200)
    last_name = models.CharField('Apellido', max_length=200)
    address = models.CharField('Dirección', max_length=50)
    rut = models.CharField('Rut', max_length=15)
    phone = models.CharField('Telefono', max_length=9)
    email = models.EmailField('Correo', max_length=150)

    class Meta:
        '''Meta definition for Cliente.'''
        ordering = ('-created', )
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{ self.first_name } { self.last_name }'
    
    @property
    def get_full_name(self):
        return f'{ self.first_name } { self.last_name }'