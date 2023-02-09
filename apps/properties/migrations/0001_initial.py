# Generated by Django 4.1.1 on 2023-02-09 18:45

import apps.properties.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Commune",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Comuna")),
                ("location_slug", models.SlugField()),
            ],
            options={"verbose_name": "Commune", "verbose_name_plural": "Communes",},
        ),
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Nombre o Razón Social"
                    ),
                ),
                ("rut", models.CharField(max_length=15, verbose_name="Rut")),
                ("phone1", models.CharField(max_length=9, verbose_name="Telefono 1")),
                (
                    "phone2",
                    models.CharField(
                        blank=True, max_length=9, verbose_name="Telefono 2"
                    ),
                ),
                ("email", models.EmailField(max_length=150, verbose_name="Correo")),
            ],
            options={"verbose_name": "Owner", "verbose_name_plural": "Owners",},
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pu", "Publicado"),
                            ("dr", "No Publicado"),
                            ("bu", "Vendido"),
                            ("re", "Arrendado"),
                            ("res", "Arrendado por Temporada"),
                            ("ex", "Permutado"),
                        ],
                        default="dr",
                        max_length=3,
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("de", "Departamento"),
                            ("ca", "Casa"),
                            ("of", "Oficina"),
                            ("lc", "Local Comercial"),
                            ("su", "Sitio Urbano"),
                            ("pa", "Parcela"),
                            ("in", "Industrial"),
                            ("bo", "Bodega"),
                            ("es", "Estacionamiento"),
                            ("va", "Vacacional"),
                        ],
                        max_length=2,
                        verbose_name="Tipo de Propiedad",
                    ),
                ),
                (
                    "publish_type",
                    models.CharField(
                        choices=[
                            ("", "Seleccione un tipo"),
                            ("ve", "Venta"),
                            ("ar", "Arriendo"),
                            ("at", "Arriendo Temporada"),
                            ("pe", "Permuta"),
                        ],
                        max_length=2,
                        verbose_name="Tipo de Operación",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100, verbose_name="Titulo(hasta 100 caracteres)"
                    ),
                ),
                ("description", models.TextField(verbose_name="Descripción")),
                (
                    "type_price",
                    models.CharField(
                        choices=[
                            ("", "Seleccione un tipo"),
                            ("uf", "UF"),
                            ("usd", "USD"),
                            ("clp", "CLP"),
                        ],
                        max_length=3,
                        verbose_name="Tipo Moneda",
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(verbose_name="Precio Publicación"),
                ),
                (
                    "appraisal_value",
                    models.PositiveIntegerField(verbose_name="Valor Tasación"),
                ),
                (
                    "commission_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        verbose_name="Porcentaje Comisión",
                    ),
                ),
                (
                    "commission_value",
                    models.PositiveIntegerField(verbose_name="Valor Comisión"),
                ),
                (
                    "google_url",
                    models.TextField(
                        blank=True, null=True, verbose_name="Ubicación en Google Maps"
                    ),
                ),
                (
                    "video_url",
                    models.URLField(blank=True, null=True, verbose_name="Video"),
                ),
                (
                    "is_featured",
                    models.BooleanField(default=False, verbose_name="Destacada"),
                ),
                ("is_new", models.BooleanField(default=False, verbose_name="Nueva")),
                ("is_iva", models.BooleanField(default=False, verbose_name="IVA")),
                (
                    "street_address",
                    models.CharField(max_length=50, verbose_name="Calle"),
                ),
                ("slug", models.SlugField(unique=True)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "commune",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to="properties.commune",
                        verbose_name="Comuna",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties_owner",
                        to="properties.owner",
                        verbose_name="Propietario",
                    ),
                ),
            ],
            options={"verbose_name": "Property", "verbose_name_plural": "Properties",},
        ),
        migrations.CreateModel(
            name="Realtor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                ("first_name", models.CharField(max_length=200, verbose_name="Nombre")),
                (
                    "last_name",
                    models.CharField(max_length=200, verbose_name="Apellido"),
                ),
                ("phone1", models.CharField(max_length=9, verbose_name="Telefono 1")),
                (
                    "phone2",
                    models.CharField(
                        blank=True, max_length=9, verbose_name="Telefono 2"
                    ),
                ),
                ("email", models.EmailField(max_length=150, verbose_name="Correo")),
            ],
            options={"verbose_name": "Realtor", "verbose_name_plural": "Realtors",},
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Comuna")),
            ],
            options={"verbose_name": "Region", "verbose_name_plural": "Regions",},
        ),
        migrations.CreateModel(
            name="PropertyManager",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "type_property",
                    models.CharField(max_length=100, verbose_name="Tipo de Propiedad"),
                ),
                ("total", models.CharField(max_length=100, verbose_name="Total")),
                (
                    "commission_percentage",
                    models.PositiveIntegerField(
                        verbose_name="Porcentaje Comisión(Valor Entero)"
                    ),
                ),
                ("commission_value", models.PositiveIntegerField()),
                (
                    "is_commission_paid",
                    models.BooleanField(default=False, verbose_name="Comisión Pagada"),
                ),
                (
                    "property",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managers",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "PropertyManager",
                "verbose_name_plural": "PropertyManagers",
            },
        ),
        migrations.CreateModel(
            name="PropertyImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.properties.models.property_images_directory_path
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "PropertyImage",
                "verbose_name_plural": "PropertyImages",
            },
        ),
        migrations.CreateModel(
            name="PropertyContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Nombre Completo"),
                ),
                ("from_email", models.EmailField(max_length=50, verbose_name="Email")),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=9, verbose_name="Télefono(opcional)"
                    ),
                ),
                ("message", models.TextField(verbose_name="Mensaje")),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property_contacts",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "PropertyContact",
                "verbose_name_plural": "PropertyContacts",
            },
        ),
        migrations.AddField(
            model_name="property",
            name="realtor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties_realtor",
                to="properties.realtor",
                verbose_name="Agente",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to="properties.region",
                verbose_name="Región",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="House",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "land_surface",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Superficie terreno (m²)"
                    ),
                ),
                (
                    "builded_surface",
                    models.PositiveIntegerField(
                        verbose_name="Superficie construida (m²)"
                    ),
                ),
                (
                    "num_rooms",
                    models.CharField(
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        verbose_name="Dormitorios",
                    ),
                ),
                (
                    "num_bathrooms",
                    models.CharField(
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        verbose_name="Baños",
                    ),
                ),
                (
                    "num_parkings",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        null=True,
                        verbose_name="Estacionamientos",
                    ),
                ),
                (
                    "num_cellars",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        null=True,
                        verbose_name="Bodegas",
                    ),
                ),
                (
                    "num_floors",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Selecione una opción"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                        ],
                        max_length=2,
                        null=True,
                        verbose_name="Pisos",
                    ),
                ),
                (
                    "num_house",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Número Casa"
                    ),
                ),
                (
                    "builded_year",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Año de Construcción"
                    ),
                ),
                (
                    "common_expenses",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Gastos comunes"
                    ),
                ),
                (
                    "distribution",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Baño Visita", "Baño Visita"),
                            ("Hall", "Hall"),
                            ("Antejardin", "Antejardin"),
                            ("Patio de Servicio", "Patio de Servicio"),
                            ("Estar de Servicio", "Estar de Servicio"),
                            ("Jardin", "Jardin"),
                            ("Despensa", "Despensa"),
                            ("Sala Estar", "Sala Estar"),
                            ("Quincho", "Quincho"),
                            ("Lavadero Interior", "Lavadero Interior"),
                            ("Lavadero Exterior", "Lavadero Exterior"),
                            ("Escritorio", "Escritorio"),
                            ("Mansarda", "Mansarda"),
                            ("Terraza", "Terraza"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Espacios Adicionales",
                    ),
                ),
                (
                    "service",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Internet", "Internet"),
                            ("Luz", "Luz"),
                            ("Agua Potable", "Agua Potable"),
                            ("Alcantarillado", "Alcantarillado"),
                            ("Alarma", "Alarma"),
                            ("Telefono", "Telefono"),
                            ("Riego Automatico", "Riego Automatico"),
                            ("Porton Automatico", "Porton Automatico"),
                            ("TV Cable", "TV Cable"),
                            ("Chimenea", "Chimenea"),
                            ("Calefaccion", "Calefaccion"),
                            ("Aire Acondicionado", "Aire Acondicionado"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Servicios",
                    ),
                ),
                (
                    "kitchen",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Comedor Diario", "Comedor Diario"),
                            ("Cocina Equipada", "Cocina Equipada"),
                            ("Cocina Amoblada", "Cocina Amoblada"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Cocina",
                    ),
                ),
                (
                    "other",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Persianas", "Persianas"),
                            ("Protecciones Ventana", "Protecciones Ventana"),
                            ("Termopaneles", "Termopaneles"),
                            ("Jacuzzi", "Jacuzzi"),
                            ("Piscina", "Piscina"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Otros",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="houses",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "House",
                "verbose_name_plural": "Houses",
                "ordering": ("-created",),
            },
        ),
        migrations.AddField(
            model_name="commune",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="communes",
                to="properties.region",
            ),
        ),
        migrations.CreateModel(
            name="Apartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.BooleanField(default=True, verbose_name="Estado")),
                (
                    "created",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de Creación"
                    ),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now=True, verbose_name="Fecha de Modificaión"
                    ),
                ),
                (
                    "land_surface",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Superficie terreno (m²)"
                    ),
                ),
                (
                    "builded_surface",
                    models.PositiveIntegerField(
                        verbose_name="Superficie construida (m²)"
                    ),
                ),
                (
                    "num_rooms",
                    models.CharField(
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        verbose_name="Dormitorios",
                    ),
                ),
                (
                    "num_bathrooms",
                    models.CharField(
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        verbose_name="Baños",
                    ),
                ),
                (
                    "num_parkings",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Selecione una opción"),
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("9", "9"),
                            ("10", "10"),
                            ("11", "11"),
                            ("12", "12"),
                            ("13", "13"),
                            ("14", "14"),
                            ("15", "15"),
                        ],
                        max_length=2,
                        null=True,
                        verbose_name="Estacionamientos",
                    ),
                ),
                (
                    "num_apartment",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Número Depto"
                    ),
                ),
                (
                    "builded_year",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Año de Construcción"
                    ),
                ),
                (
                    "common_expenses",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Gastos comunes"
                    ),
                ),
                (
                    "distribution",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Baño Visita", "Baño Visita"),
                            ("Hall", "Hall"),
                            ("Antejardin", "Antejardin"),
                            ("Patio de Servicio", "Patio de Servicio"),
                            ("Estar de Servicio", "Estar de Servicio"),
                            ("Jardin", "Jardin"),
                            ("Despensa", "Despensa"),
                            ("Sala Estar", "Sala Estar"),
                            ("Quincho", "Quincho"),
                            ("Lavadero Interior", "Lavadero Interior"),
                            ("Lavadero Exterior", "Lavadero Exterior"),
                            ("Escritorio", "Escritorio"),
                            ("Mansarda", "Mansarda"),
                            ("Terraza", "Terraza"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Espacios Adicionales",
                    ),
                ),
                (
                    "service",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Internet", "Internet"),
                            ("Luz", "Luz"),
                            ("Agua Potable", "Agua Potable"),
                            ("Alcantarillado", "Alcantarillado"),
                            ("Alarma", "Alarma"),
                            ("Telefono", "Telefono"),
                            ("Riego Automatico", "Riego Automatico"),
                            ("Porton Automatico", "Porton Automatico"),
                            ("TV Cable", "TV Cable"),
                            ("Chimenea", "Chimenea"),
                            ("Calefaccion", "Calefaccion"),
                            ("Aire Acondicionado", "Aire Acondicionado"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Servicios",
                    ),
                ),
                (
                    "kitchen",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Comedor Diario", "Comedor Diario"),
                            ("Cocina Equipada", "Cocina Equipada"),
                            ("Cocina Amoblada", "Cocina Amoblada"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Cocina",
                    ),
                ),
                (
                    "other",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("Persianas", "Persianas"),
                            ("Protecciones Ventana", "Protecciones Ventana"),
                            ("Termopaneles", "Termopaneles"),
                            ("Jacuzzi", "Jacuzzi"),
                            ("Piscina", "Piscina"),
                        ],
                        default="",
                        max_length=250,
                        verbose_name="Otros",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apartments",
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "Apartment",
                "verbose_name_plural": "Apartments",
                "ordering": ("-created",),
            },
        ),
    ]