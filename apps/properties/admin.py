from django.contrib import admin
from .models import House, Property, Apartment, PropertyImage, Region, Commune, PropertyContact, Realtor, Owner, PropertyManager

# Register your models here.
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage


class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        PropertyImageInline,
    ]
    list_display = ("title", "street_address" , "property_type", "publish_type", "type_price", 'price', 'uuid', 'state')

# admin.site.register(House, HouseAdmin)
# admin.site.register(Apartment, ApartmentAdmin)
# admin.site.register(Location)


admin.site.register(PropertyManager)
admin.site.register(PropertyContact)
admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(House)
admin.site.register(Apartment)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Realtor)
admin.site.register(Owner)

