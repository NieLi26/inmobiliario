import os
from pathlib import Path
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from apps.properties.models import Publication
from .models import OperationBuyHistory


@receiver(pre_save, sender=OperationBuyHistory)
def operation_buy_history_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            antigua_instancia = OperationBuyHistory.objects.get(pk=instance.pk)
            if antigua_instancia.purchase_sale_agreement != instance.purchase_sale_agreement:
                delete_file(antigua_instancia.purchase_sale_agreement)
            if antigua_instancia.sales_document != instance.sales_document:
                delete_file(antigua_instancia.sales_document)
        except OperationBuyHistory.DoesNotExist:
            pass
    # path_file = instance.purchase_sale_agreement.path
    # delete_file(path_file)



@receiver(post_save, sender=OperationBuyHistory)
def operation_buy_history_post_save(sender, instance, created, **kwargs):
    if created:
        instance.publication.operation = Publication.Operations.FINISHED
        instance.publication.save()


@receiver(pre_delete, sender=OperationBuyHistory)
def operation_buy_history_pre_delete(sender, instance, **kwargs):
    if instance.purchase_sale_agreement:
        delete_file(instance.purchase_sale_agreement)
    if instance.sales_document:
        delete_file(instance.sales_document)


    # Check if the image exists
    # if os.path.exists(image):
        # delete image
        # fs = FileSystemStorage()
        # fs.delete(image)
    # else:
    #     pass
    #     print('Archivo no existe')

# forma 1
def delete_file(file):
    path = Path(file.path)
    if path.is_file():
        path.unlink()

# forma 2
# def delete_file(file):
#     if os.path.isfile(file.path):
#         os.remove(file.path)