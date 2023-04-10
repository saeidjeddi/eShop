from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCod
from django.contrib.auth.models import Group



# Register your models here.

admin.site.site_header = 'پنل مدیریت وبسایت'


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'phone_number', 'full_name', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'full_name', 'password')}),
        ('ویژگی ها', {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {"fields": ('username', 'phone_number', 'email', 'full_name', 'password1', 'password2')}),
    )
    search_fields = ('username', 'email', 'full_name', 'phone_number')
    ordering = ('username', 'email', 'full_name', 'phone_number')
    list_per_page = 4
    readonly_fields = ('last_login',)

    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        is_admin = request.user.is_admin
        is_active = request.user.is_active
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_admin'].disabled = True
            form.base_fields['is_active'].disabled = True
        return form


admin.site.register(User, UserAdmin)



@admin.register(OtpCod)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'jalali')
    search_fields = ('phone_number', 'code')
    list_per_page = 3



