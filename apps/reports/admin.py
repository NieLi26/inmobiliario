from django.contrib import admin

from .models import OperationBuyHistory

# Register your models here.

@admin.register(OperationBuyHistory)
class OperationBuyHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_sale_advance', 'publication', 'total', 'is_commission_paid', 'state')
    raw_id_fields = ['publication'] 


# class EspecialidadInline(admin.TabularInline):
#     model = Especialidad


# @admin.register(Categoria)
# class CategoriaAdmin(admin.ModelAdmin):
#     inlines = [
#         EspecialidadInline
#     ]
#     list_display = ('nombre', 'is_active')


# @admin.register(Especialidad)
# class EspecialidadAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'categoria', 'tarifa', 'is_active')
#     raw_id_fields = ['tarifa', 'categoria']  # Crea una barra de busqueda en el campo