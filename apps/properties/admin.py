from django.contrib import admin
from .models import (
    House, Property, Apartment,
    PropertyImage, Region, Commune,
    PropertyContact, Realtor, Owner,
    Publication, Office, Shop,
    Cellar, Industrial, UrbanSite,
    Parcel
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage


class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        PropertyImageInline,
    ]
    list_display = ("title", "street_address", "property_type", "publish_type",  'uuid', 'is_active')


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("property", "type_price", 'price', 'operation', 'status', 'state')

# admin.site.register(House, HouseAdmin)
# admin.site.register(Apartment, ApartmentAdmin)
# admin.site.register(Location)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(House)
admin.site.register(Apartment)
admin.site.register(Office)
admin.site.register(Shop)
admin.site.register(Cellar)
admin.site.register(Industrial)
admin.site.register(UrbanSite)
admin.site.register(Parcel)
admin.site.register(PropertyContact)
admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(Realtor)
admin.site.register(Owner)

