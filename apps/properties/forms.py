import re
import random
from django import forms
from django.utils.text import slugify
from datetime import date
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.accounts.rut_chile import is_valid_rut

from .models import (
    House, Property, Apartment,
    Commune, Region, PropertyContact,
    Realtor, Owner, Office, UrbanSite,
    Parcel, Industrial, Cellar, Shop,
    Publication
)

from .validators import (
    LowerCase,
    UpperCase,
    Capitalize,
    number_validator,
    number_decimal_validator,
    email_validator,
    attrs_class,
    attrs_class_error,
)


class PublicationBaseForm(forms.ModelForm):

    price = forms.CharField(
        label='Precio Publicación',
        validators=[number_validator],
        error_messages={'required': 'Este campo no puede estar vacio.'},
        help_text='Este es un texto de ayuda! ir a <a href="/">Home<a/>'
    )
    commission_value = forms.CharField(
        label='Monto Comision',
        validators=[number_validator]
    )

    def __init__(self, *args, **kwargs):
        self.publish_type = kwargs.pop('publish_type', None) 
        self.user = kwargs.pop('user', None)
        print(self.publish_type)
        super().__init__(*args, **kwargs)

        # ========== ADVANCE CONTROL PANEL (multiple <inputs>) ========== |

        for field in self.fields:
            attrs = {}
            if field != 'is_featured' and field != 'is_new' and field != 'is_iva':
                attrs['class'] = attrs_class
            else:
                attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"

            if self.errors.get(field):
                attrs['class'] = attrs_class_error
            self.fields[field].widget.attrs.update(attrs)

        selects = ['owner', 'realtor']
        for select in selects:
            self.fields[select].widget.attrs['form'] = 'form-general'

       # ========== BASIC CONTROL PANEL (single <inputs>) ========== |

        self.fields['owner'].queryset = Owner.objects.filter(state=True)
        self.fields['realtor'].queryset = Realtor.objects.filter(state=True)

        self.fields['price'].widget.attrs['x-mask:dynamic'] = '$money($input)' # no funciona en todos    
        if self.publish_type != 'ar' and self.publish_type != 'at':
            self.fields['commission_value'].widget.attrs['readonly'] = 'true'

    # mas seguro y puedes restringir que no se pueda cambiar un valor, en este caso el usuario, ya que la instancia si se puede modificar
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class PublicationForm(PublicationBaseForm):

    appraisal_value = forms.CharField(
        label='Valor Tasación',
        validators=[number_validator],
        required=False
    )
    commission_percentage = forms.CharField(
        label='Porcentaje Comisión',
        validators=[number_decimal_validator],
    )

    class Meta:
        model = Publication
        fields = (
            'owner',
            'realtor',
            'type_price',
            'price',
            'appraisal_value',
            'commission_percentage',
            'commission_value',
            'is_iva',
            'is_featured'
        )


class PublicationRentForm(PublicationBaseForm):
    class Meta:
        model = Publication
        fields = (
            'owner',
            'realtor',
            'type_price',
            'price',
            'commission_value',
            'is_iva',
            'is_featured'
        )


# ========== BASE PROPERTY, PROPERTY RENT ========== |
class PropertyBaseForm(forms.ModelForm):
    # se le puede poner cualquier nombre, y cualquier texto, y se llama con el nombre del contexto como pasaste el form.nombre de la variable(ej. form.required_css_class)
    required_css_class = 'focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700' 

    # INSIDE WIDGETS

    # si no creara este atributo solo me denegaria automaticamente el valor que no es numero, y me diria siempre "el valor es requerido"
    google_url = forms.CharField(
        label='Google url',
        widget=forms.TextInput(attrs={
                'placeholder': 'copiar enlace de incorporacion de mapa'
            }),
        required=False
    )
    title = Capitalize(
        label='Titulo(hasta 100 caracteres)',
        widget=forms.TextInput(attrs={
                'placeholder': 'Ingrese un titulo'
            }
        )
    )

    # ------------------------------------------------ SUPER FUNCTION ------------------------------------------------ |

    def __init__(self, *args, **kwargs):
        self.publish_type = kwargs.pop('publish_type', None) 
        self.property_type = kwargs.pop('property_type', None) 
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


       # ========== BASIC CONTROL PANEL (single <inputs>) ========== |

        # ERROR MESSAGES
        # self.fields['description'].error_messages.update({'required': 'No puede estar sin nada'})

        self.fields['description'].widget.attrs['rows'] = '3'

        # form 1
        # self.fields['property_type'].widget.attrs['style'] = 'display:none'
        # self.fields['property_type'].widget.attrs.update(style='display:none')
        # self.fields['property_type'].initial = property_type

        region_data = {
            'hx-get': '/properties/commune-select',
            'hx-trigger': 'change delay:500ms',
            'hx-target': '#communes',
        }
        self.fields['region'].widget.attrs.update(region_data)

        self.fields['video_url'].widget.attrs['class'] = 'focus:outline-none border border-gray-300 rounded-r-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'

        # self.fields['commune'].initial = commune
        # self.fields['commune'].widget.attrs['class'] += ' bg-gray-200'
        # self.fields['commune'].widget.attrs['disabled'] = '{% if disabled %}true{% else %}false{% endif %}'

        # ========== ADVANCE CONTROL PANEL (multiple <inputs>) ========== |
        
        # # ERROR MESSAGES
        # for field in self.fields:
        #     self.fields[field].error_messages.update({'required': 'No puede estar sin nada'})
        
        for field in self.fields:
            attrs = {}
            if field != 'is_new':
                attrs['class'] = attrs_class
            else:
                attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
            # if self.errors.get(field) and self.fields[field].widget.attrs.get('class'):
            if self.errors.get(field):
                attrs['class'] = attrs_class_error
            self.fields[field].widget.attrs.update(attrs)

        # selects = ['owner', 'realtor']
        for selects in self.fields:
            self.fields[selects].widget.attrs['form'] = 'form-general'


 

        # ------------------------------------------------ SUPER FUNCTION END ------------------------------------------------ |

    # more_images = forms.FileField(required=True, label='Mas Imagenes',widget=forms.ClearableFileInput(attrs={
    #     'multiple': True,
    #     'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
    # }))

    def has_class_attr(self):
        # Check if the title field widget has a class attr
        for field in self.fields:
            if 'class' in self.fields[field].widget.attrs:
                print(field)
        return False

    class Meta:
        model = Property
        # si se quiere asignar valor en formulario debe estar en fields, pero esto te obliga a poner el input en el template o modificarlo en el metodo clean
        # sino lo pasas en el fields debes pasarlo como argumento del formulario, asigarlo a alguna variable que tu puedes crear por ejmplo 'sef.lo_que_sea', luego lo asignas donde quieras
        fields = ( 
            'title',
            'description',
            # 'type_price',
            # 'price',
            'google_url',
            'video_url',
            # 'is_featured',
            'is_new',
            # 'is_active',
            # 'is_iva',
            'region',
            'commune',
            'street_address',
            'street_number',
            # 'realtor',
            # 'owner',
            # 'appraisal_value',  # null(valor tasacion)
            # 'commission_percentage',  # null(porcentaje comision)
            # 'commission_value',
            'common_expenses',
            'num_roll'
        )

        # OUTSIDE WIDGETS        
        # widgets ={
        #     'commune': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        #     'google_url': forms.TextInput(attrs={'placeholder': 'copiar enlace de incorporacion de mapa'}),
        # }


    # ------------------------------------------------ FUNCTION (METHOD CLEAN) ------------------------------------------------ |

    # def clean_street_address(self):
    #     street_address = self.cleaned_data['street_address']
    #     if len(street_address) < 100:
    #         raise forms.ValidationError('Muy pocos parametros') 
    #     return street_address


    # def clean_price(self):
    #     price = self.cleaned_data['price']
    #     if price <= 0:
    #         msg = 'Precio debe ser mayor a cero'
    #         raise forms.ValidationError(msg) 
    #     return price



    # esta es parecida al metodo save, pero solo cuando la instancia no se volvera a modificar, pq podria causar errores
    # def create(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.user = self.request.user
    #     if commit:
    #         instance.save()
    #     return instance

    # mas seguro y puedes restringir que no se pueda cambiar un valor, en este caso el usuario, ya que la instancia si se puede modificar
    def save(self, commit=True, property_type=None):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.user = self.user
            instance.property_type = self.property_type
            instance.publish_type = self.publish_type
        if commit:
            instance.save()
        return instance


class PropertyForm(PropertyBaseForm):
    pass
    # appraisal_value = forms.CharField(
    #     label='Valor Tasación',
    #     validators=[number_validator]
    # )
    # commission_percentage = forms.CharField(
    #     label='Porcentaje Comision',
    #     validators=[number_decimal_validator]
    # )


class PropertyRentForm(PropertyBaseForm):
    class Meta:
        model = Property
        fields = ( 
            'title',
            'description',
            # 'type_price',
            # 'price',
            'google_url',
            'video_url',
            # 'is_featured',
            'is_new',
            # 'is_iva',
            'region',
            'commune',
            'street_address',
            'street_number',
            # 'realtor',
            # 'owner',
            # 'commission_value',
            'common_expenses',
            'num_roll'
        )

# ========== BASE HOUSE, APARTMENT, OFFICE ========== |


class HAOBaseForm(forms.ModelForm):
    land_surface = forms.IntegerField(
        label='Superficie terreno (m²)',
        validators=[number_validator],
        required=False,
        widget=forms.TextInput()
    )
    builded_surface = forms.IntegerField(
        label='Superficie construida (m²)',
        validators=[number_validator],
        widget=forms.TextInput()
    )
    builded_year = forms.IntegerField(
        label='Año de Construcción',
        validators=[number_validator],
        required=False,
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'distribution' and field != 'service' and field != 'kitchen' and field != 'other':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

    # VALIDATIONS
    # la "r" significa que la cadena string sera tratada como un "raw string" lo que no procesara las combinaciones especiales con backslash "\" 
    # land_surface = forms.IntegerField(label='Superficie de terreno', validators=[RegexValidator(r'^[0-9]*$', message='Solo numeros son permitidos')], required=False)

    def clean_builded_year(self):
        builded_year = self.cleaned_data.get('builded_year')
        if builded_year and int(builded_year) > date.today().year:
            msg = 'El año de construcción debe ser igual o inferior al actual'
            raise forms.ValidationError(msg)
        return builded_year

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     builded_year = cleaned_data.get('builded_year')
    #     builded_surface = cleaned_data.get('builded_surface')
    #     land_surface = cleaned_data.get('land_surface')
    #     if builded_year is not None and builded_year > date.today().year:
    #         msg = 'El año de construcción debe ser igual o inferior al actual'
    #         self.add_error('builded_year', msg)
    #     if builded_surface is not None and builded_surface <= 0:
    #         msg = 'Superficie construida debe ser mayor a cero'
    #         self.add_error('builded_surface', msg)
    #     if land_surface is not None and land_surface <= 0:
    #         msg = 'Superficie de terreno debe ser mayor a cero'
    #         self.add_error('land_surface', msg)


class HouseForm(HAOBaseForm):

    class Meta:
        model = House
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_rooms',
            'num_bathrooms',
            'num_parkings',
            'num_cellars',
            'num_floors',
            'num_house',
            'builded_year',
            'distribution',
            'service',
            'kitchen',
            'other'
        )


class ApartmentForm(HAOBaseForm):

    class Meta:
        model = Apartment
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_rooms',
            'num_bathrooms',
            'num_parkings',
            'num_apartment',
            'builded_year',
            'distribution',
            'service',
            'kitchen',
            'other'
        )


class OfficeForm(HAOBaseForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field != 'distribution' and field != 'service' and field != 'kitchen':
    #             self.fields[field].widget.attrs['class'] = attrs_class
    #         if self.errors.get(field):
    #             self.fields[field].widget.attrs['class'] = attrs_class_error

    class Meta:
        model = Office
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_offices',
            'num_bathrooms',
            'num_parkings',
            'num_cellars',
            'num_floors',
            'num_local',
            'builded_year',
            'distribution',
            'service',
            'kitchen'
        )


class ShopForm(HAOBaseForm):
    land_surface = forms.CharField(
        label='Superficie terreno (m²)',
        validators=[number_validator],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'service' and field != 'kitchen':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

    class Meta:
        model = Shop
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_bathrooms',
            'num_local',
            'builded_year',
            'service',
            'kitchen',
        )

# ========== BASE CELLAR, INDUSTRIAL ========== |


class CIBaseForm(forms.ModelForm):
    land_surface = forms.CharField(
        label='Superficie terreno (m²)',
        validators=[number_validator],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'distribution' and field != 'service' and field != 'kitchen':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error


class CellarForm(CIBaseForm):
    class Meta:
        model = Cellar
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_bathrooms',
            'num_offices',
            'num_local',
            'num_enclosures'
        )


class IndustrialForm(CIBaseForm):
    class Meta:
        model = Industrial
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_bathrooms',
            'num_offices',
            'num_local',
            'num_cellars'
        )


# ========== BASE URBAN SITE, PARCEL ========== |


class UPBaseForm(forms.ModelForm):

    Yes_Or_No = (
        ('si', 'Si'),
        ('no', 'No')
    )

    land_surface = forms.CharField(
        label='Superficie terreno (m²)',
        validators=[number_validator]
    )
    water_feasibility = forms.CharField(label='Factibilidad Agua', widget=forms.RadioSelect(choices=Yes_Or_No))
    electricity_feasibility = forms.CharField(label='Factibilidad Electricidad', widget=forms.RadioSelect(choices=Yes_Or_No))
    sewer_feasibility = forms.CharField(label='Factibilidad Alcantarillado', widget=forms.RadioSelect(choices=Yes_Or_No))
    gas_feasibility = forms.CharField(label='Factibilidad Gas', widget=forms.RadioSelect(choices=Yes_Or_No))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'distribution' and field != 'service' and field != 'kitchen' and field != 'water_feasibility' and field != 'electricity_feasibility' and field != 'sewer_feasibility' and field != 'gas_feasibility':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                if field != 'water_feasibility' and field != 'electricity_feasibility' and field != 'sewer_feasibility' and field != 'gas_feasibility':
                    self.fields[field].widget.attrs['class'] = attrs_class_error
                
        self.fields['feasibility'].widget.attrs['rows'] = '3'


class UrbanSiteForm(UPBaseForm):

    class Meta:
        model = UrbanSite
        fields = (
            'property',
            'land_surface',
            'num_cellars',
            'num_lot',
            'sector',
            'feasibility',
            'water_feasibility',
            'electricity_feasibility',
            'sewer_feasibility',
            'gas_feasibility'
        )


class ParcelForm(UPBaseForm):
    class Meta:
        model = Parcel
        fields = (
            'property',
            'land_surface',
            'num_cellars',
            'num_lot',
            'sector',
            'feasibility',
            'water_feasibility',
            'electricity_feasibility',
            'sewer_feasibility',
            'gas_feasibility'
        )

# ========== OTHERS ========== |


class PropertyContactForm(forms.ModelForm):
    
    class Meta:
        model = PropertyContact
        fields = ('name', 'from_email', 'phone', 'message')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '':
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone


class RealtorForm(forms.ModelForm):
    email = LowerCase(
        label='Correo Electronico',
        validators=[email_validator]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

    class Meta:
        model = Realtor
        fields = ('first_name', 'last_name', 'phone1', 'email')


class OwnerForm(forms.ModelForm):

    email = LowerCase(
        label='Correo Electronico',
        validators=[email_validator]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

        data = {
            # 'x-mask': '99999999-*',
            'placeholder': 'Ej. 99999999-9',
        }
        self.fields['rut'].widget.attrs.update(data)
        # self.fields['rut'].widget.attrs['class'] += ' uppercase' 

    rut = UpperCase(required=True)

    class Meta:
        model = Owner
        fields = ('name', 'rut', 'phone1', 'email')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        msg = ["El rut es invalido", "Ingrese sin puntos y con guion"]
        try:
            if not is_valid_rut(rut):
                msg = "El rut es invalido"
                raise forms.ValidationError(msg)
        except:
            raise forms.ValidationError(msg)
        return rut