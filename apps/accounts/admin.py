from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    AuthenticationForm
)

from .forms import CustomUserCreationForm, CustomUserChangeForm, AdminCreationForm
from .models import CustomUser, AgentProfile, AdminProfile, Admin


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_active', 'tipo', 'rut')


# class AdminAdmin(admin.ModelAdmin):
#     add_form = AdminCreationForm
#     # form = CustomUserChangeForm
#     model = Admin


admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register(Admin, AdminAdmin)

# admin.site.register(Pricing, PricingAdmin)


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'start_contract', 'end_contract')

    @admin.display(description='User Username', ordering='user__username')
    def get_user_username(self, obj):
        return obj.user.username


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_username',)

    @admin.display(description='User Username', ordering='user__username')
    def get_user_username(self, obj):
        return obj.user.username
