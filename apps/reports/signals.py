from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from apps.properties.models import Publication

from .models import OperationBuyHistory
from .utils import delete_file


@receiver(pre_save, sender=OperationBuyHistory)
def operation_buy_history_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            antigua_instancia = OperationBuyHistory.objects.get(pk=instance.pk)
            if antigua_instancia.purchase_sale_agreement and antigua_instancia.purchase_sale_agreement != instance.purchase_sale_agreement:
                delete_file(antigua_instancia.purchase_sale_agreement)
            if antigua_instancia.sales_document and antigua_instancia.sales_document != instance.sales_document:
                delete_file(antigua_instancia.sales_document)
        except OperationBuyHistory.DoesNotExist:
            pass


@receiver(pre_delete, sender=OperationBuyHistory)
def operation_buy_history_pre_delete(sender, instance, **kwargs):
    if instance.purchase_sale_agreement:
        delete_file(instance.purchase_sale_agreement)
    if instance.sales_document:
        delete_file(instance.sales_document)
