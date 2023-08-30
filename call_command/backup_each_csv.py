'''
django standalone script to take backup of database in the form of csvs for each model.
- Place it in the same directory as manage.py file
- Rename PROJECT_NAME to your project's name
'''

import os

PROJECT_NAME = 'core'


def main():
    from django.apps import apps
    import csv

    # Obtener una lista de todos los modelos en la aplicación Django.
    model_list = apps.get_models()
    model_name_list = [x.__name__ for x in model_list]
    
    # se iteran los modelos
    for model in model_list:
        # se obtienen todos los campos del modelo
        all_fields = model._meta.get_fields()
        # se crea un array con los nombres de los campos del modelo
        columns = [x.name for x in all_fields]
        
        # comprobamos si el directorio "csvs" existe y sino se crea
        if not os.path.exists('csvs'):
            os.makedirs('csvs')

        # se abre(crea) un archivo con extension ".csv" en modo escritura ("w")
        with open(f'csvs/{model.__name__}.csv', mode='w') as csv_file:
            # crea un objeto escritor CSV que se utilizara para escribir datos del modelo en el archivo ".csv" que se abrio
            # pide en archivo ".csv", demiliter="separacion", 
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Escribir nombre de columnas en la primera fila del archivo ".csv"
            writer.writerow(columns)

            # Obtener todas las instancias de la clase o objetos del modelo
            objects = model.objects.all()
            
            # Iteramos sobre cada instancia
            for obj in objects:
                # se crea una lista de valores de fila para cada campo del objeto. Si el campo no tiene un valor, se utiliza la cadena "NA"
                row = [str(getattr(obj, field_name, "NA")) for field_name in columns]
                # se escribe la lista de valores de fila en el archivo CSV utilizando el objeto writer.
                writer.writerow(row)
    

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django
    django.setup()
    main()