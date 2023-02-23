import os
import random
import string

from django.forms import model_to_dict
import uuid 
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL, AUTH_USER_MODEL
from django.urls import reverse
from PIL import Image

from django.utils.text import slugify

User = AUTH_USER_MODEL

# multi select
from multiselectfield import MultiSelectField

from apps.base.models import TimeStampedModel

# def property_directory_path(instance,filename):
#     return 'property/{0}/{1}'.format(instance.uuid, filename)


def property_images_directory_path(instance,filename):
    return 'property_images/{0}/{1}'.format(instance.property.uuid, filename)


def create_unique_slug(model_instance, slug_field_name):
    # Creamos un slug a partir del título del elemento
    slug = slugify(model_instance.title)

    # Verificamos si existe un elemento con ese slug
    class_ = model_instance.__class__
    count = 0
    while class_.objects.filter(**{slug_field_name: slug}).exclude(pk=model_instance.pk).exists():
        # Si existe, agregamos una combinación de letras y números al final para hacerlo único
        slug += '-' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        count += 1
        if count > 100:
            # Evitamos bucles infinitos
            break
    # Asignamos el slug único al objeto
    model_instance.slug = slug


class IpVisitor(TimeStampedModel):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Realtor(TimeStampedModel):
    '''Model definition for Realtor.'''
    first_name = models.CharField('Nombre', max_length=200)
    last_name = models.CharField('Apellido', max_length=200)
    phone1 = models.CharField('Telefono 1', max_length=9)
    phone2 = models.CharField('Telefono 2', max_length=9, blank=True)
    email = models.EmailField('Correo', max_length=150)
    class Meta:
        '''Meta definition for Realtor.'''

        verbose_name = 'Realtor'
        verbose_name_plural = 'Realtors'

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('properties:realtor_detail', kwargs={'pk': self.pk})


class Owner(TimeStampedModel):
    '''Model definition for Owner.'''
    name = models.CharField('Nombre o Razón Social', max_length=200)
    rut = models.CharField('Rut', max_length=15)
    phone1 = models.CharField('Telefono 1', max_length=9)
    phone2 = models.CharField('Telefono 2', max_length=9, blank=True)
    email = models.EmailField('Correo', max_length=150)
    class Meta:
        '''Meta definition for Owner.'''

        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'

    def __str__(self):
        return '{0} / {1}'.format(self.name, self.rut)


class Property(TimeStampedModel):
    '''Model definition for Property.'''

    PROPERTY_APARTMENT = 'de'
    PROPERTY_HOUSE = 'ca'
    PROPERTY_OFFICE = 'of'
    PROPERTY_SHOP = 'lc'
    PROPERTY_URBAN_SITE = 'su'
    PROPERTY_PARCEL = 'pa'
    PROPERTY_INDUSTRIAL = 'in'
    PROPERTY_CELLAR = 'bo'
    # PROPERTY_PARKING = 'es'
    # PROPERTY_VACATION = 'va'

    PROPERTY_CHOICES = (
        (PROPERTY_APARTMENT, 'Departamento'),
        (PROPERTY_HOUSE, 'Casa'),
        (PROPERTY_OFFICE, 'Oficina'),
        (PROPERTY_SHOP, 'Local Comercial'),
        (PROPERTY_URBAN_SITE, 'Sitio Urbano'),
        (PROPERTY_PARCEL, 'Parcela'),
        (PROPERTY_INDUSTRIAL, 'Industrial'),
        (PROPERTY_CELLAR, 'Bodega'),
        # (PROPERTY_PARKING, 'Estacionamiento'),
        # (PROPERTY_VACATION, 'Vacacional'),
    )

    PUBLISH_BUY = 've'
    PUBLISH_RENT = 'ar'
    PUBLISH_RENTAL_SEASON = 'at'
    PUBLISH_EXCHANGE = 'pe'

    PUBLISH_CHOICES = (
        ('', 'Seleccione un tipo'),
        (PUBLISH_BUY, 'Venta'),
        (PUBLISH_RENT, 'Arriendo'),
        (PUBLISH_RENTAL_SEASON, 'Arriendo Temporada'),
        (PUBLISH_EXCHANGE, 'Permuta')
    )

    TYPE_PRICE_CHOICES = (
        ('', 'Seleccione un tipo'),
        ('uf', 'UF'),
        ('usd', 'USD'),
        ('clp', 'CLP'),
    )

    class Status(models.TextChoices):
        PUBLISH = 'pu', 'Publicado' # green
        DRAFT = 'dr', 'No Publicado' # red
        # BUY = 'bu', 'Vendido' 
        # RENT = 're', 'Arrendado'
        # RENTAL_SEASON = 'res', 'Arrendado por Temporada'
        # EXCHANGE = 'ex', 'Permutado'

    # General
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties_user')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties_owner', verbose_name='Propietario')
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name='properties_realtor', verbose_name='Agente')
    status = models.CharField(choices=Status.choices, max_length=3, default=Status.DRAFT)
    property_type = models.CharField('Tipo de Propiedad', choices=PROPERTY_CHOICES, max_length=2)
    publish_type = models.CharField('Tipo de Operación', choices=PUBLISH_CHOICES, max_length=2)
    title = models.CharField("Titulo(hasta 100 caracteres)", max_length=100)
    description = models.TextField("Descripción")
    type_price = models.CharField('Tipo Moneda', choices=TYPE_PRICE_CHOICES, max_length=3)
    price = models.PositiveIntegerField('Precio Publicación')
    appraisal_value = models.PositiveIntegerField('Valor Tasación', null=True, blank=True)
    commission_percentage = models.DecimalField('Porcentaje Comisión', null=True, blank=True, decimal_places=2, max_digits=4)
    commission_value = models.PositiveIntegerField('Monto Comisión')
    common_expenses = models.PositiveIntegerField('Gastos comunes', blank=True, null=True)

    # url externas
    google_url = models.TextField('Ubicación en Google Maps', blank=True, null=True)
    video_url = models.URLField('Video', blank=True, null=True)

    # status
    is_featured = models.BooleanField('Destacada', default=False)
    is_new = models.BooleanField('Nueva', default=False)
    is_iva = models.BooleanField('IVA', default=False)

    # miniatura
    # thumbnail = models.ImageField('Imagen',upload_to=property_directory_path, blank=True)

    # locacion
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Región', related_name='properties')
    commune = models.ForeignKey('Commune', on_delete=models.CASCADE, verbose_name='Comuna', related_name='properties')
    street_address = models.CharField("Calle", max_length=50)
    street_number = models.CharField("Numero Calle", max_length=50)

    # SII
    num_roll = models.CharField('Numero de Rol(SII)', max_length=50)

    # extras for urls
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # get visitors
    views = models.ManyToManyField(IpVisitor, related_name="property_ip_visitor")
    
    class Meta:
        '''Meta definition for Property.'''

        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    # def save(self, *args, **kwargs): # se debe hacer aqui si es un valor que se va a dar por default, pq el clean del modelo no lo toma el cambio
    #     if not self.id:
    #         self.state = False
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Generamos un slug único para el objeto
        create_unique_slug(self, 'slug')
        # Guardamos el objeto en la base de datos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_property_type_display()} - {self.title}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_absolute_url(self):
        return reverse("properties:property_detail", kwargs={"publish_type": self.publish_type, "property_type": self.property_type, 'location_slug': self.commune.location_slug,"slug": self.slug, 'uuid': self.uuid})

    # actuca sobre la clase, considerando todas sus instancias
    # El primer argumento de un método de clase debe ser la propia clase, que se pasa automáticamente como argumento(en este caso "cls").
    @classmethod
    def count_by_user(cls, user):
        return cls.objects.filter(user=user).count()
    
    @property
    def get_views(self):
        return self.views.count()
    

class PropertyImage(TimeStampedModel):
    '''Model definition for PropertyImage.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties')
    image = models.ImageField(upload_to=property_images_directory_path)

    class Meta:
        '''Meta definition for PropertyImage.'''

        verbose_name = 'PropertyImage'
        verbose_name_plural = 'PropertyImages'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        im = Image.open(self.image.path)


        # new resizing
        new_height = 720
        new_width = int(new_height / im.height * im.width)
        new_size = Image.new("RGB", (new_width, new_height), color="white")
        new_size.paste(im.resize((new_width, new_height)), (0, 0))

        # save new image
        # new_image_path = self.image.path.split(".")[0] + "_resized.jpg"
        new_image_path = self.image.path
        new_size.save(new_image_path, "JPEG", quality=90)

        # resizing 
        # new_height = 720
        # new_width = int(new_height / im.height * im.width)
        # new_size = im.resize((new_width, new_height))
        # new_size.save(self.image.path)

    # def delete(self):
    #     # opcion 1
    #     image = self.image.path
    #     if os.path.isfile(image):
    #         os.remove(image)
    #     #opcion 2
    #     self.image.delete()
    #     return super().delete()

    def __str__(self):
        return self.property.title

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, "img/empty.png")
    
    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item


class House(TimeStampedModel):

    class Others(models.TextChoices):
        BLINDS = 'Persianas', 'Persianas'
        WINDOW_PROTECTIONS = 'Protecciones Ventana', 'Protecciones Ventana'
        THERMOPANELS = 'Termopaneles', 'Termopaneles'
        JACUZZI = 'Jacuzzi', 'Jacuzzi'
        SWIMMING_POOL = 'Piscina', 'Piscina'

    class AdditionalSpaces(models.TextChoices):
        BATHROOM_VISIT = 'Baño Visita', 'Baño Visita'
        HALL = 'Hall', 'Hall'
        GARDEN_SUEDE = 'Antejardin', 'Antejardin'
        SERVICE_YARD = 'Patio de Servicio', 'Patio de Servicio'
        SERVICE_ROOM = 'Estar de Servicio', 'Estar de Servicio'
        GARDEN = 'Jardin', 'Jardin'
        PANTRY = 'Despensa', 'Despensa'
        LIVING_ROOM = 'Sala Estar', 'Sala Estar'
        QUNCHO = 'Quincho', 'Quincho'
        INDOOR_LAUNDRY = 'Lavadero Interior', 'Lavadero Interior'
        OUTDOOR_LAUNDRY = 'Lavadero Exterior', 'Lavadero Exterior'
        DESK = 'Escritorio', 'Escritorio'
        MANSARD = 'Mansarda', 'Mansarda'
        TERRACE = 'Terraza', 'Terraza'

    class Services(models.TextChoices):
        INTERNET = 'Internet', 'Internet'
        LIGHT = 'Luz', 'Luz'
        DRINKING_WATER = 'Agua Potable', 'Agua Potable'
        SEWER_SYSTEM = 'Alcantarillado', 'Alcantarillado'
        ALARM = 'Alarma', 'Alarma'
        PHONE = 'Telefono', 'Telefono'
        AUTOMATIC_IRRIGATION = 'Riego Automatico', 'Riego Automatico'
        AUTOMATIC_DOOR = 'Porton Automatico', 'Porton Automatico'
        TV = 'TV Cable', 'TV Cable'
        CHIMNEY = 'Chimenea', 'Chimenea'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'
  
    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'

    class Quantitys(models.TextChoices):
        VALUE = '','Selecione una opción'
        VALUE_0 = '0','0'
        VALUE_1 = '1','1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    class QuantityFloors(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'


    '''Model definition for House.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='houses', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)", blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_rooms = models.CharField('Dormitorios', choices=Quantitys.choices, max_length=2)
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_parkings = models.CharField('Estacionamientos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_cellars = models.CharField('Bodegas', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_floors = models.CharField('Pisos', choices=QuantityFloors.choices, blank=True, null=True, max_length=2)
    num_house = models.CharField("Número Casa", blank=True, max_length=20)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True)

    distribution = MultiSelectField('Espacios Adicionales', choices=AdditionalSpaces.choices, max_length=250, default="", blank=True)
    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="", blank=True)
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="", blank=True)
    other = MultiSelectField('Otros',choices=Others.choices , max_length=250, default="", blank=True)




    class Meta:
        '''Meta definition for House.'''

        ordering = ('-created',)
        verbose_name = 'House'
        verbose_name_plural = 'Houses'

    def __str__(self):
        return self.property.title


class Apartment(TimeStampedModel):

    class Others(models.TextChoices):
        BLINDS = 'Persianas', 'Persianas'
        WINDOW_PROTECTIONS = 'Protecciones Ventana', 'Protecciones Ventana'
        THERMOPANELS = 'Termopaneles', 'Termopaneles'
        JACUZZI = 'Jacuzzi', 'Jacuzzi'
        SWIMMING_POOL = 'Piscina', 'Piscina'

    class AdditionalSpaces(models.TextChoices):
        BATHROOM_VISIT= 'Baño Visita', 'Baño Visita'
        HALL = 'Hall', 'Hall'
        GARDEN_SUEDE = 'Antejardin', 'Antejardin'
        SERVICE_YARD = 'Patio de Servicio', 'Patio de Servicio'
        SERVICE_ROOM = 'Estar de Servicio', 'Estar de Servicio'
        GARDEN = 'Jardin', 'Jardin'
        PANTRY = 'Despensa', 'Despensa'
        LIVING_ROOM = 'Sala Estar', 'Sala Estar'
        QUNCHO = 'Quincho', 'Quincho'
        INDOOR_LAUNDRY = 'Lavadero Interior', 'Lavadero Interior'
        OUTDOOR_LAUNDRY = 'Lavadero Exterior', 'Lavadero Exterior'
        DESK = 'Escritorio', 'Escritorio'
        MANSARD = 'Mansarda', 'Mansarda'
        TERRACE = 'Terraza', 'Terraza'

    class Services(models.TextChoices):
        INTERNET = 'Internet', 'Internet'
        LIGHT = 'Luz', 'Luz'
        DRINKING_WATER = 'Agua Potable', 'Agua Potable'
        SEWER_SYSTEM = 'Alcantarillado', 'Alcantarillado'
        ALARM = 'Alarma', 'Alarma'
        PHONE = 'Telefono', 'Telefono'
        AUTOMATIC_IRRIGATION = 'Riego Automatico', 'Riego Automatico'
        AUTOMATIC_DOOR = 'Porton Automatico', 'Porton Automatico'
        TV = 'TV Cable', 'TV Cable'
        CHIMNEY = 'Chimenea', 'Chimenea'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'
        
    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN  = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'

    class Quantitys(models.TextChoices):
        VALUE = '','Selecione una opción'
        VALUE_0 = '0','0'
        VALUE_1 = '1','1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    '''Model definition for Apartment.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='apartments', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)", blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_rooms = models.CharField('Dormitorios', choices=Quantitys.choices, max_length=2)
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_parkings = models.CharField('Estacionamientos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_apartment = models.CharField("Número Depto", blank=True, max_length=20)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True)

    distribution = MultiSelectField('Espacios Adicionales', choices=AdditionalSpaces.choices, max_length=250, default="", blank=True)
    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="", blank=True)
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="", blank=True)
    other = MultiSelectField('Otros',choices=Others.choices , max_length=250, default="", blank=True)

    class Meta:
        '''Meta definition for Apartment.'''

        ordering = ('-created',)
        verbose_name = 'Apartment'
        verbose_name_plural = 'Apartments'

    def __str__(self):
        return self.property.title


class Office(TimeStampedModel):

    class AdditionalSpaces(models.TextChoices):
        HALL = 'Hall', 'Hall'
        SERVICE_YARD = 'Patio de Servicio', 'Patio de Servicio'
        GARDEN = 'Jardin', 'Jardin'
        LIVING_ROOM = 'Sala Estar', 'Sala Estar'

    class Services(models.TextChoices):
        INTERNET = 'Internet', 'Internet'
        LIGHT = 'Luz', 'Luz'
        DRINKING_WATER = 'Agua Potable', 'Agua Potable'
        SEWER_SYSTEM = 'Alcantarillado', 'Alcantarillado'
        ALARM = 'Alarma', 'Alarma'
        PHONE = 'Telefono', 'Telefono'
        AUTOMATIC_IRRIGATION = 'Riego Automatico', 'Riego Automatico'
        AUTOMATIC_DOOR = 'Porton Automatico', 'Porton Automatico'
        AUTOMATIC_BLIND = 'Persianas Automaticas', 'Persianas Automaticas'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'
        
    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN  = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    '''Model definition for Office.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offices', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)", blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_offices = models.CharField('Oficinas', choices=Quantitys.choices, max_length=2)
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_parkings = models.CharField('Estacionamientos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_cellars = models.CharField('Bodegas/Recintos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_floors = models.CharField('Pisos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_local = models.CharField("Número de Local", blank=True, max_length=20)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True)

    distribution = MultiSelectField('Espacios Adicionales', choices=AdditionalSpaces.choices, max_length=250, default="", blank=True)
    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="", blank=True)
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="", blank=True)

    class Meta:
        '''Meta definition for Office.'''

        ordering = ('-created',)
        verbose_name = 'Office'
        verbose_name_plural = 'Offices'

    def __str__(self):
        return self.property.title


class Shop(TimeStampedModel):
    '''Model definition for Shop.'''
    class Services(models.TextChoices):
        INTERNET = 'Internet', 'Internet'
        LIGHT = 'Luz', 'Luz'
        DRINKING_WATER = 'Agua Potable', 'Agua Potable'
        SEWER_SYSTEM = 'Alcantarillado', 'Alcantarillado'
        ALARM = 'Alarma', 'Alarma'
        PHONE = 'Telefono', 'Telefono'
        TV = 'TV Cable', 'TV Cable'
        CHIMNEY = 'Chimenea', 'Chimenea'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'

    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='shops', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_local = models.CharField("Número de Local", blank=True, max_length=20)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True)

    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="", blank=True)
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="", blank=True)

    class Meta:
        '''Meta definition for Shop.'''

        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return self.title


class Cellar(TimeStampedModel):
    '''Model definition for Cellar.'''

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='cellars', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_enclosures = models.CharField('Recintos', choices=Quantitys.choices,  max_length=2)
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_offices = models.CharField('Oficinas', choices=Quantitys.choices, max_length=2)
    num_local = models.CharField("Número de Local", blank=True, max_length=20)

    class Meta:
        '''Meta definition for Cellar.'''

        verbose_name = 'Cellar'
        verbose_name_plural = 'Cellars'

    def __str__(self):
        return self.title


class Industrial(TimeStampedModel):
    '''Model definition for Industrial.'''

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='industrials', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    num_cellars = models.CharField('Bodegas', choices=Quantitys.choices,  max_length=2)
    num_bathrooms = models.CharField('Baños', choices=Quantitys.choices, max_length=2)
    num_offices = models.CharField('Oficinas', choices=Quantitys.choices, max_length=2)
    num_local = models.CharField("Número de Local", blank=True, max_length=20)

    class Meta:
        '''Meta definition for Industrial.'''

        verbose_name = 'Industrial'
        verbose_name_plural = 'Industrials'

    def __str__(self):
        return self.title


class UrbanSite(TimeStampedModel):
    '''Model definition for UrbanSite.'''

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    class YesOrNo(models.TextChoices):
        YES = 'si', 'Si'
        NO = 'no', 'No'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='urban_sites', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    num_cellars = models.CharField('Bodegas/Recintos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_lot = models.CharField("Número de Lote", max_length=20)
    sector = models.CharField("Sector", max_length=250)
    water_feasibility = models.CharField('Factibilidad Agua', choices=YesOrNo.choices, max_length=2)
    electricity_feasibility = models.CharField('Factibilidad Electricidad', choices=YesOrNo.choices, max_length=2)
    sewer_feasibility = models.CharField('Factibilidad Alcantarillado', choices=YesOrNo.choices, max_length=2)
    gas_feasibility = models.CharField('Factibilidad Gas', choices=YesOrNo.choices, max_length=2)
    feasibility = models.TextField(verbose_name="Factibilidad")

    class Meta:
        '''Meta definition for UrbanSite.'''

        verbose_name = 'UrbanSite'
        verbose_name_plural = 'UrbanSites'

    def __str__(self):
        return self.title


class Parcel(TimeStampedModel):
    '''Model definition for Parcel.'''

    class Quantitys(models.TextChoices):
        VALUE = '', 'Selecione una opción'
        VALUE_0 = '0', '0'
        VALUE_1 = '1', '1'
        VALUE_2 = '2', '2'
        VALUE_3 = '3', '3'
        VALUE_4 = '4', '4'
        VALUE_5 = '5', '5'
        VALUE_6 = '6', '6'
        VALUE_7 = '7', '7'
        VALUE_8 = '8', '8'
        VALUE_9 = '9', '9'
        VALUE_10 = '10', '10'
        VALUE_11 = '11', '11'
        VALUE_12 = '12', '12'
        VALUE_13 = '13', '13'
        VALUE_14 = '14', '14'
        VALUE_15 = '15', '15'

    class YesOrNo(models.TextChoices):
        YES = 'si', 'Si'
        NO = 'no', 'No'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='parcels', blank=True, null=True)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    num_cellars = models.CharField('Bodegas/Recintos', choices=Quantitys.choices, blank=True, null=True, max_length=2)
    num_lot = models.CharField("Número de Lote", max_length=20)
    sector = models.CharField("Sector", max_length=250)
    water_feasibility = models.CharField('Factibilidad Agua', choices=YesOrNo.choices, max_length=2)
    electricity_feasibility = models.CharField('Factibilidad Electricidad', choices=YesOrNo.choices, max_length=2)
    sewer_feasibility = models.CharField('Factibilidad Alcantarillado', choices=YesOrNo.choices, max_length=2)
    gas_feasibility = models.CharField('Factibilidad Gas', choices=YesOrNo.choices, max_length=2)
    feasibility = models.TextField(verbose_name="Factibilidad")

    class Meta:
        '''Meta definition for Parcel.'''

        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'

    def __str__(self):
        return self.title


class Region(TimeStampedModel):

    '''Model definition for Region.'''
    name = models.CharField('Comuna', max_length=150)

    class Meta:
        '''Meta definition for Region.'''

        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class Commune(TimeStampedModel):
    '''Model definition for Commune.'''
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='communes')
    name = models.CharField('Comuna', max_length=150)
    location_slug = models.SlugField()
    class Meta:
        '''Meta definition for Commune.'''

        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'

    def __str__(self):
        return self.name

    def get_commune_region(self):
        return f"{self.name}, {self.region}"


class PropertyContact(TimeStampedModel):
    '''Model definition for PropertyContact.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_contacts')
    name = models.CharField('Nombre Completo', max_length=200)
    from_email = models.EmailField('Email', max_length=50)
    phone = models.CharField('Télefono(opcional)', max_length=9, blank=True)
    message = models.TextField('Mensaje')

    class Meta:
        '''Meta definition for PropertyContact.'''

        verbose_name = 'PropertyContact'
        verbose_name_plural = 'PropertyContacts'

    def __str__(self):
        return str(self.from_email)


class PropertyManager(TimeStampedModel):
    '''Model definition for PropertyManager.'''
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, related_name='managers', blank=True, null=True)
    type_property = models.CharField('Tipo de Propiedad', max_length=100)
    total = models.CharField('Total', max_length=100)
    commission_percentage = models.PositiveIntegerField('Porcentaje Comisión(Valor Entero)')
    commission_value = models.PositiveIntegerField()
    is_commission_paid = models.BooleanField('Comisión Pagada', default=False)
    class Meta:
        '''Meta definition for PropertyManager.'''

        verbose_name = 'PropertyManager'
        verbose_name_plural = 'PropertyManagers'

    def __str__(self):
        return self.type_property