import os
from django.db import models
from apps.base.models import TimeStampedModel
import uuid
from apps.properties.models import Publication
from .validators import ext_validator
from .utils import (
    operation_buy_purchase_sale_files_directory_path,
    operation_buy_sales_document_files_directory_path,
    operation_rent_lease_files_directory_path,
    operation_rent_guarantee_document_files_directory_path
)
from apps.crm.models import Client


class OperationBuyHistory(TimeStampedModel):
    '''Model definition for OperationHistory.'''
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='operations_buy', blank=True, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='operations_buy')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchase_sale_advance = models.PositiveIntegerField('Anticipo de Compra/Venta', default=0, null=True, blank=True)
    purchase_sale_agreement = models.FileField('Promesa de Compra/Venta',
                                               upload_to=operation_buy_purchase_sale_files_directory_path,
                                               blank=True, null=True,
                                               validators=[ext_validator])
    signature_purchase_sale_agreement = models.DateField('Fecha Firma Promesa de Compra/Venta', null=True, blank=True)
    sales_document = models.FileField('Contrato de Compra/Venta',
                                      upload_to=operation_buy_sales_document_files_directory_path,
                                      blank=True, null=True,
                                      validators=[ext_validator])
    signature_sales_document = models.DateField('Fecha Firma Contrato de Pago', null=True, blank=True)
    total = models.PositiveIntegerField('Total', default=0)
    total_commission = models.PositiveIntegerField('Total Comision', default=0)
    is_commission_paid = models.BooleanField('Comisión Pagada', default=False)
    has_promise = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)  # preguntar si se necesita este campo

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

    @property
    def is_editabled(self):
        if self.total > 0:
            return True
        return False


class ActiveRentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)


class OperationRent(TimeStampedModel):
    '''Model definition for OperationRent.'''
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='operations_rent', blank=True, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='operations_rent')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    guarantee_value = models.PositiveIntegerField('Valor de Garantia', default=0)
    guarantee_document = models.FileField('Documento de Garantia',
                                               upload_to=operation_rent_guarantee_document_files_directory_path,
                                               blank=True, null=True,
                                               validators=[ext_validator])
    lease_agreement = models.FileField('Contrato de Arriendo',
                                               upload_to=operation_rent_lease_files_directory_path,
                                               blank=True, null=True,
                                               validators=[ext_validator])
    signature_lease_agreement = models.DateField('Fecha Firma Contrato de Arriendo', null=True, blank=True)
    lease_start_date = models.DateField('Fecha Inicio Contrato Arriendo', null=True, blank=True)
    lease_final_date = models.DateField('Fecha Termino Contrato Arriendo', null=True, blank=True)
    monthly_total = models.PositiveIntegerField('Total Arriendo Mensual', default=0)
    is_lease_commission_paid = models.BooleanField('Comisión por Contrato Pagada', default=False)
    monthly_commission = models.PositiveIntegerField('Total Comision', default=0)
    is_completed = models.BooleanField(default=False)  # preguntar si se necesita este campo
    active_objects = ActiveRentManager()
    objects = models.Manager()

    class Meta:
        '''Meta definition for OperationRent.'''
        # Especifica el nombre del manager base (original)
        default_manager_name = 'objects'
        verbose_name = 'OperationRent'
        verbose_name_plural = 'OperationRents'

    def __str__(self):
        return str(self.publication.property.property_type)

    # @property
    # def get_real_comission(self):
    #     return round((self.total * self.publication.commission_percentage) / 100)


class PaymentRent(TimeStampedModel):
    '''Model definition for PaymentRent.'''
    operation_rent = models.ForeignKey(OperationRent, on_delete=models.CASCADE, related_name='payments_rent')
    total_payment = models.PositiveIntegerField('Total', default=0)
    payment_date = models.DateField('Fecha de Pago')
    is_commission_paid = models.BooleanField('Comisión Pagada', default=False)
    is_partial_payment = models.BooleanField('Pago Parcial', default=False)

    class Meta:
        '''Meta definition for PaymentRent.'''
        ordering = ('-payment_date',)
        verbose_name = 'PaymentRent'
        verbose_name_plural = 'PaymentRents'

    def __str__(self):
        return str(self.operation_rent.uuid)