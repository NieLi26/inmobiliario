from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.properties.models import Region, Commune


class Command(BaseCommand):
    help = 'Load Region and Communes'

    def handle(self, *args, **kwargs):
        # COMUNNE
        Commune.objects.all().delete()
        region_names = [
            'Metropolitana',
            'Antofagasta',
            'Araucanía',
            'Arica y Parinatoca',
            'Atacama',
            'Aysén',
            'Bernardo Ohiggins',
            'Biobío',
            'Coquimbo',
            'Los Lagos',
            'Los Ríos',
            'Magallanes',
            'Maule',
            'Ñuble',
            'Tarapacá',
            'Valparaíso',
        ]

        if not Region.objects.count():
            for region_name in region_names:
                Region.objects.create(name=region_name)

        # Metropolitana
        met = Region.objects.get(name='Metropolitana')

        metropolitana_commune = [
            'Tiltil',
            'Lampa',
            'Colina',
            'San José de Maipo',
            'Puente Alto',
            'Pirque',
            'San Bernardo',
            'Paine',
            'Calera de Tango',
            'Buin',
            'San Pedro',
            'Melipilla',
            'María Pinto',
            'Curacaví',
            'Alhué',
            'Vitacura',
            'Santiago',
            'San Ramón',
            'San Miguel',
            'San Joaquín',
            'Renca',
            'Recoleta',
            'Quinta Normal',
            'Quilicura',
            'Pudahuel',
            'Providencia',
            'Peñalolén',
            'Pedro Aguirre Cerda',
            'Ñuñoa',
            'Maipú',
            'Macul',
            'Lo Prado',
            'Lo Espejo',
            'Lo Barnechea',
            'Las Condes',
            'La Reina',
            'La Pintana',
            'La Granja',
            'La Florida',
            'La Cisterna',
            'Independencia',
            'Huechuraba',
            'Estación Central',
            'El Bosque',
            'Conchalí',
            'Cerro Navia',
            'Cerrillos',
            'Talagante',
            'Peñaflor',
            'Padre Hurtado',
            'Isla de Maipo',
            'El Monte',
        ]

        for commune in metropolitana_commune:
            Commune.objects.create(name=commune, region=met, location_slug=slugify(f"{commune}-{met}"))

        # Antofagasta
        an = Region.objects.get(name='Antofagasta')

        antofagasta_commune = [
            'Taltal',
            'Sierra Gorda',
            'Mejillones',
            'Antofagasta',
            'San Pedro de Atacama',
            'Ollagüe',
            'Calama',
            'Tocopilla',
            'María Elena',
        ]

        for commune in antofagasta_commune:
            Commune.objects.create(name=commune, region=an, location_slug=slugify(f"{commune}-{an}"))

        # Araucanía
        ar = Region.objects.get(name='Araucanía')

        araucania_commune = [
            'Villarrica',
            'Vilcún',
            'Toltén',
            'Teodoro Schmidt',
            'Temuco',
            'Saavedra',
            'Pucón',
            'Pitrufquén',
            'Perquenco',
            'Padre Las Casas',
            'Nueva Imperial',
            'Melipeuco',
            'Loncoche',
            'Lautaro',
            'Gorbea',
            'Galvarino',
            'Freire',
            'Curarrehue',
            'Cunco',
            'Cholchol',
            'Carahue',
            'Victoria',
            'Traiguén',
            'Renaico',
            'Purén',
            'Lumaco',
            'Los Sauces',
            'Lonquimay',
            'Ercilla',
            'Curacautín',
            'Collipulli',
            'Angol',
        ]

        for commune in araucania_commune:
            Commune.objects.create(name=commune, region=ar, location_slug=slugify(f"{commune}-{ar}"))

        # Arica y Parinatoca
        ap = Region.objects.get(name='Arica y Parinatoca')

        arica_y_parinatoca_commune = [
            'Camarones',
            'Arica',
            'Putre',
            'General Lagos',
        ]

        for commune in arica_y_parinatoca_commune:
            Commune.objects.create(name=commune, region=ap, location_slug=slugify(f"{commune}-{ap}"))

        # Atacama
        at = Region.objects.get(name='Atacama')

        atacama_commune = [
            'Diego de Almagro',
            'Chañaral',
            'Tierra Amarilla',
            'Copiapó',
            'Caldera',
            'Vallenar',
            'Huasco',
            'Freirina',
            'Alto del Carmen',
        ]

        for commune in atacama_commune:
            Commune.objects.create(name=commune, region=at, location_slug=slugify(f"{commune}-{at}"))

        # Aysén
        ay = Region.objects.get(name='Aysén')

        aysen_commune = [
            'Guaitecas',
            'Cisnes',
            'Aysén',
            'Tortel',
            'O Higgins',
            'Cochrane',
            'Lago Verde',
            'Coihaique',
            'Río Ibáñez',
            'Chile Chico',
        ]

        for commune in aysen_commune:
            Commune.objects.create(name=commune, region=ay, location_slug=slugify(f"{commune}-{ay}"))

        # Bernardo Ohiggins
        bo = Region.objects.get(name='Bernardo Ohiggins')

        bernardo_ohiggins_commune = [
            'San Vicente',
            'Requínoa',
            'Rengo',
            'Rancagua',
            'Quinta de Tilcoco',
            'Pichidegua',
            'Peumo',
            'Olivar',
            'Mostazal',
            'Malloa',
            'Machalí',
            'Las Cabras',
            'Graneros',
            'Doñihue',
            'Coltauco',
            'Coinco',
            'Codegua',
            'Pichilemu',
            'Paredones',
            'Navidad',
            'Marchihue',
            'Litueche',
            'La Estrella',
            'Santa Cruz',
            'San Fernando',
            'Pumanque',
            'Placilla',
            'Peralillo',
            'Palmilla',
            'Nancagua',
            'Lolol',
            'Chimbarongo',
            'Chépica',
        ]

        for commune in bernardo_ohiggins_commune:
            Commune.objects.create(name=commune, region=bo, location_slug=slugify(f"{commune}-{bo}"))

        # Biobío
        bb = Region.objects.get(name='Biobío')

        bio_bio_commune = [
            'Tirúa',
            'Los Álamos',
            'Lebu',
            'Curanilahue',
            'Contulmo',
            'Cañete',
            'Arauco',
            'Yumbel',
            'Tucapel',
            'Santa Bárbara',
            'San Rosendo',
            'Quilleco',
            'Quilaco',
            'Negrete',
            'Nacimiento',
            'Mulchén',
            'Los Ángeles',
            'Laja',
            'Cabrero',
            'Antuco',
            'Alto Biobío',
            'Tomé',
            'Talcahuano',
            'Santa Juana',
            'San Pedro de la Paz',
            'Penco',
            'Lota',
            'Hualqui',
            'Hualpén',
            'Florida',
            'Coronel',
            'Concepción',
            'Chiguayante',
        ]

        for commune in bio_bio_commune:
            Commune.objects.create(name=commune, region=bb, location_slug=slugify(f"{commune}-{bb}"))

        # Coquimbo
        co = Region.objects.get(name='Coquimbo')

        coquimbo_commune = [
            'Salamanca',
            'Los Vilos',
            'Illapel',
            'Canela',
            'Vicuña',
            'Paiguano',
            'La Serena',
            'La Higuera',
            'Coquimbo',
            'Andacollo',
            'Río Hurtado',
            'Punitaqui',
            'Ovalle',
            'Monte Patria',
            'Combarbalá',
        ]

        for commune in coquimbo_commune:
            Commune.objects.create(name=commune, region=co, location_slug=slugify(f"{commune}-{co}"))

        # Los Lagos
        ll = Region.objects.get(name='Los Lagos')

        los_lagos_commune = [
            'Quinchao',
            'Quemchi',
            'Quellón',
            'Queilén',
            'Puqueldón',
            'Dalcahue',
            'Curaco de Vélez',
            'Chonchi',
            'Castro',
            'Ancud',
            'Puerto Varas',
            'Puerto Montt',
            'Maullín',
            'Los Muermos',
            'Llanquihue',
            'Frutillar',
            'Fresia',
            'Cochamó',
            'Calbuco',
            'San Pablo',
            'San Juan de la Costa',
            'Río Negro',
            'Puyehue',
            'Purranque',
            'Puerto Octay',
            'Osorno',
            'Palena',
            'Hualaihué',
            'Futaleufú',
            'Chaitén',
        ]

        for commune in los_lagos_commune:
            Commune.objects.create(name=commune, region=ll, location_slug=slugify(f"{commune}-{ll}"))

        # Los Ríos
        lr = Region.objects.get(name='Los Ríos')

        los_rios_commune = [
            'Río Bueno',
            'Lago Ranco',
            'La Unión',
            'Futrono',
            'Valdivia',
            'Panguipulli',
            'Paillaco',
            'Mariquina',
            'Máfil',
            'Los Lagos',
            'Lanco',
            'Corral',
        ]

        for commune in los_rios_commune:
            Commune.objects.create(name=commune, region=lr, location_slug=slugify(f"{commune}-{lr}"))

        # Magallanes
        ma = Region.objects.get(name='Magallanes')

        magallanes_commune = [
            'Cabo de Hornos',
            'Antártica',
            'San Gregorio',
            'Río Verde',
            'Punta Arenas',
            'Laguna Blanca',
            'Timaukel',
            'Primavera',
            'Porvenir',
            'Torres del Paine',
            'Natales',
        ]

        for commune in magallanes_commune:
            Commune.objects.create(name=commune, region=ma, location_slug=slugify(f"{commune}-{ma}"))

        # Maule
        mau = Region.objects.get(name='Maule')

        maule_commune = [
            'Pelluhue',
            'Chanco',
            'Cauquenes',
            'Vichuquén',
            'Teno',
            'Sagrada Familia',
            'Romeral',
            'Rauco',
            'Molina',
            'Licantén',
            'Hualañé',
            'Curicó',
            'Yerbas Buenas',
            'Villa Alegre',
            'San Javier',
            'Retiro',
            'Parral',
            'Longaví',
            'Linares',
            'Colbún',
            'Talca',
            'San Rafael',
            'San Clemente',
            'Río Claro',
            'Pencahue',
            'Pelarco',
            'Maule',
            'Empedrado',
            'Curepto',
            'Constitución',
        ]

        for commune in maule_commune:
            Commune.objects.create(name=commune, region=mau, location_slug=slugify(f"{commune}-{mau}"))

        # Ñuble
        nu = Region.objects.get(name='Ñuble')

        nuble_commune = [
            'Pelluhue',
            'Chanco',
            'Cauquenes',
            'Vichuquén',
            'Teno',
            'Sagrada Familia',
            'Romeral',
            'Rauco',
            'Molina',
            'Licantén',
            'Hualañé',
            'Curicó',
            'Yerbas Buenas',
            'Villa Alegre',
            'San Javier',
            'Retiro',
            'Parral',
            'Longaví',
            'Linares',
            'Colbún',
            'Talca',
            'San Rafael',
            'San Clemente',
            'Río Claro',
            'Pencahue',
            'Pelarco',
            'Maule',
            'Empedrado',
            'Curepto',
            'Constitución',
        ]

        for commune in nuble_commune:
            Commune.objects.create(name=commune, region=nu, location_slug=slugify(f"{commune}-{nu}"))

        # Tarapaca
        ta = Region.objects.get(name='Tarapacá')

        tarapaca_commune = [
            'Iquique',
            'Alto Hospicio',
            'Pozo Almonte',
            'Pica',
            'Huara',
            'Colchane,'
            'Camiña',
        ]

        for commune in tarapaca_commune:
            Commune.objects.create(name=commune, region=ta, location_slug=slugify(f"{commune}-{ta}"))

        # Valparaiso
        va = Region.objects.get(name='Valparaíso')

        valparaiso_commune = [
            'Isla de Pascua',
            'San Esteban',
            'Rinconada',
            'Los Andes',
            'Calle Larga',
            'Villa Alemana',
            'Quilpué',
            'Limache',
            'Olmué',
            'Zapallar',
            'Petorca',
            'Papudo',
            'La Ligua',
            'Cabildo',
            'Quillota',
            'Nogales',
            'La Cruz',
            'La Calera',
            'Hijuelas',
            'Santo Domingo',
            'San Antonio',
            'El Tabo',
            'El Quisco',
            'Cartagena',
            'Algarrobo',
            'Santa María',
            'San Felipe',
            'Putaendo',
            'Panquehue',
            'Llaillay',
            'Catemu',
            'Viña del Mar',
            'Valparaíso',
            'Quintero',
            'Puchuncaví',
            'Concón',
            'Juan Fernández',
            'Casablanca',
        ]

        for commune in valparaiso_commune:
            Commune.objects.create(name=commune, region=va, location_slug=slugify(f"{commune}-{va}"))

        