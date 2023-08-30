import os
from django.db import models
from apps.base.models import TimeStampedModel
import uuid
from apps.properties.models import Publication
from .validators import ext_validator

# Create your models here.




def operation_buy_purchase_sale_files_directory_path(instance, filename):
    return 'operation_files/buy/{0}/purchase_sale/{1}'.format(instance.uuid, filename)


def operation_buy_sales_document_files_directory_path(instance, filename):
    return 'operation_files/buy/{0}/sales_document/{1}'.format(instance.uuid, filename)


class OperationBuyHistory(TimeStampedModel):
    '''Model definition for OperationHistory.'''
    # type_property = models.CharField('Tipo de Propiedad', max_length=2)
    # type_publish = models.CharField('Tipo de Publicación', max_length=2, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchase_sale_advance = models.PositiveIntegerField('Anticipo de Compra/Venta', default=0, null=True, blank=True)
    purchase_sale_agreement = models.FileField('Promesa de Compra/Venta',
                                               upload_to=operation_buy_purchase_sale_files_directory_path,
                                               blank=True, null=True,
                                               validators=[ext_validator])
    signature_purchase_sale_agreement = models.DateField('Fecha Promesa de Compra/Venta', null=True, blank=True)
    sales_document = models.FileField('Compra/Venta',
                                      upload_to=operation_buy_sales_document_files_directory_path,
                                      blank=True, null=True,
                                      validators=[ext_validator])
    sales_document_purchase_sale_agreement = models.DateField('Fecha Compra/Venta', null=True, blank=True)
    # operation = models.CharField('Estado de Operación', max_length=50)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='operations_buy_history')
    # codigo = models.CharField('Codigo', max_length=255)
    # region = models.CharField('Region', max_length=200)
    # commune = models.CharField('Comuna', max_length=200)
    # total = models.CharField('Total', max_length=100)
    total = models.PositiveIntegerField('Total', default=0)
    # commission_percentage = models.PositiveIntegerField('Porcentaje Comisión(Valor Entero)')
    # commission_value = models.PositiveIntegerField()
    is_commission_paid = models.BooleanField('Comisión Pagada', default=False)
    has_promise = models.BooleanField(default=False)

    class Meta:
        '''Meta definition for OperationHistory.'''

        verbose_name = 'OperationBuyHistory'
        verbose_name_plural = 'OperationsBuyHistory'

    def __str__(self):
        return str(self.publication.property.property_type)

    # @property
    # def filename(self):
    #     return os.path.basename(self.file.name)

    @property
    def get_real_comission(self):
        return round((self.total * self.publication.commission_percentage) / 100)

