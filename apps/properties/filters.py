import django_filters
from django.db.models import Q

from .models import House, Apartment, Property


class PropertyFilter(django_filters.FilterSet):

    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    ORDER_CHOICES = (
        (ORDER_ASC, 'A - Z'),
        (ORDER_DESC, 'Z - A'),
    )

    min_room = django_filters.NumberFilter(method='get_min_room')
    max_room = django_filters.NumberFilter(method='get_max_room')
    min_bathroom = django_filters.NumberFilter(method='get_min_bathroom')
    max_bathroom = django_filters.NumberFilter(method='get_max_bathroom')
    order = django_filters.ChoiceFilter(choices=ORDER_CHOICES, method='filter_by_order')
    # price = django_filters.RangeFilter()

    class Meta:
        model = Property     
        fields = {
                # 'price': ['lte', 'gte'], 
                # 'land_surface': ['lte', 'gte'],
                # 'type_price': ['exact'],
            }

    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'asc' else '-created'
        return queryset.order_by(expression)

    def get_min_bathroom(self, queryset, name, value):
        return queryset.filter(
            Q(houses__num_bathrooms__gte=value) |
            Q(apartments__num_bathrooms__gte=value) |
            Q(offices__num_bathrooms__gte=value) |
            Q(shops__num_bathrooms__gte=value) |
            Q(cellars__num_bathrooms__gte=value) |
            Q(industrials__num_bathrooms__gte=value) 
            # Q(urban_sites__num_bathrooms__gte=value) |
            # Q(parcels__num_bathrooms__gte=value) 
        ).distinct()
        # return queryset.filter(Q(houses__num_bathrooms__gte=value) | Q(apartments__num_bathrooms__gte=value))

    def get_max_bathroom(self, queryset, name, value):
        return queryset.filter(
            Q(houses__num_bathrooms__gte=value) |
            Q(apartments__num_bathrooms__gte=value) |
            Q(offices__num_bathrooms__gte=value) |
            Q(shops__num_bathrooms__gte=value) |
            Q(cellars__num_bathrooms__gte=value) |
            Q(industrials__num_bathrooms__gte=value)
        ).distinct()
        # return queryset.filter(Q(houses__num_bathrooms__lte=value) | Q(apartments__num_bathrooms__lte=value))

    def get_min_room(self, queryset, name, value):
        return queryset.filter(
            Q(houses__num_rooms__gte=value) | 
            Q(apartments__num_rooms__gte=value)
        )

    def get_max_room(self, queryset, name, value):
        return queryset.filter(
            Q(houses__num_rooms__lte=value) | 
            Q(apartments__num_rooms__lte=value)
        )


class HouseFilter(django_filters.FilterSet):    
    # SORT_BY_CREATED = 'created'
    # SORT_BY_TITLE = 'title'

    # SORT_BY_CHOICES = (
    #     (SORT_BY_CREATED, 'Fecha'),
    #     (SORT_BY_TITLE, 'Nombre'),
    # )

    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    ORDER_CHOICES = (
        (ORDER_ASC, 'A - Z'),
        (ORDER_DESC, 'Z - A'),
    )

    min_room = django_filters.NumberFilter(field_name='num_rooms', lookup_expr='gte')
    max_room = django_filters.NumberFilter(field_name='num_rooms', lookup_expr='lte')
    min_bathroom = django_filters.NumberFilter(field_name='num_bathrooms', lookup_expr='gte')
    max_bathroom = django_filters.NumberFilter(field_name='num_bathrooms', lookup_expr='lte')
    # sort_by = django_filters.ChoiceFilter(choices=SORT_BY_CHOICES, method='filter_by_sorted')
    order = django_filters.ChoiceFilter(choices=ORDER_CHOICES, method='filter_by_order')

    class Meta:
        model = House
        fields = ('property__publish_type', 'created', 'property__publish_type')    


    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'asc' else '-created'
        return queryset.order_by(expression)


    # def filter_by_sorted(self, queryset, name, value):
    #     if value == 'created':
    #         expression =  'created'
    #         # if order == 'desc':
    #         #     expression =  '-created'
    #     else:
    #         expression = 'property__title'
    #         # if order == 'desc':
    #         #     expression =  '-property__title'

    #     return queryset.order_by(expression)

    # def filter_by_order(self, queryset, name, value):
    #     order = self.filter_by_sorted(queryset, name, value)
    #     if value == 'asc':
    #         expression =  order
    #     else:
    #         expression =  order.reverse()
    #     return expression

class ApartmentFilter(django_filters.FilterSet):    
    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    ORDER_CHOICES = (
        (ORDER_ASC, 'A - Z'),
        (ORDER_DESC, 'Z - A'),
    )

    min_room = django_filters.NumberFilter(field_name='num_rooms', lookup_expr='gte')
    max_room = django_filters.NumberFilter(field_name='num_rooms', lookup_expr='lte')
    min_bathroom = django_filters.NumberFilter(field_name='num_bathrooms', lookup_expr='gte')
    max_bathroom = django_filters.NumberFilter(field_name='num_bathrooms', lookup_expr='lte')
    order = django_filters.ChoiceFilter(choices=ORDER_CHOICES, method='filter_by_order')

    class Meta:
        model = Apartment
        fields = ('property__publish_type', 'created', 'property__publish_type')    


    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'asc' else '-created'
        return queryset.order_by(expression)