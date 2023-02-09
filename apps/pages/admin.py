from django.contrib import admin

from .models import Contact, OwnerContact
# Register your models here.

# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ("property_type", "publish_type", "price", 'uf')

admin.site.register(Contact)
admin.site.register(OwnerContact)
