from django.db import models
from apps.base.models import TimeStampedModel

# Create your models here.


class OperationHistory(TimeStampedModel):
    '''Model definition for OperationHistory.'''
    type_property = models.CharField('Tipo de Propiedad', max_length=100)
    operation = models.CharField('Estado de Operación', max_length=50)
    codigo = models.CharField('Codigo', max_length=255)
    region = models.CharField('Region', max_length=200)
    commune = models.CharField('Comuna', max_length=200)
    total = models.CharField('Total', max_length=100)
    commission_percentage = models.PositiveIntegerField('Porcentaje Comisión(Valor Entero)')
    commission_value = models.PositiveIntegerField()
    is_commission_paid = models.BooleanField('Comisión Pagada', default=False)

    class Meta:
        '''Meta definition for OperationHistory.'''

        verbose_name = 'OperationHistory'
        verbose_name_plural = 'OperationsHistory'

    def __str__(self):
        return self.type_property
