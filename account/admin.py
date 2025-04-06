from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    exclude = ('password',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login', )
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_header = "Teco Admin"
admin.site.site_title = "Teco Admin Portal"