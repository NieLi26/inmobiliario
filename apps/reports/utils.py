import os
from pathlib import Path


# forma 1
def delete_file(file):
    ''' Recibe archivo '''
    path = Path(file.path)
    if path.is_file():
        path.unlink()

# forma 2
# def delete_file(file):
#     ''' Recibe Archivo '''
#     if os.path.isfile(file.path):
#         os.remove(file.path)


# VENTAS

def operation_buy_purchase_sale_files_directory_path(instance, filename):
    return 'operation_files/buy/{0}/purchase_sale/{1}'.format(instance.uuid, filename)


def operation_buy_sales_document_files_directory_path(instance, filename):
    return 'operation_files/buy/{0}/sales_document/{1}'.format(instance.uuid, filename)


# ARRIENDO

def operation_rent_lease_files_directory_path(instance, filename):
    return 'operation_files/rent/{0}/lease/{1}'.format(instance.uuid, filename)


def operation_rent_guarantee_document_files_directory_path(instance, filename):
    return 'operation_files/buy/{0}/guarantee_document/{1}'.format(instance.uuid, filename)