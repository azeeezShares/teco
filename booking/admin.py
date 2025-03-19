from django.contrib import admin
from .models import Branch, Service, Booking, Client, Admin

admin.site.register(Branch)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('branch',)  # Improves usability for ManyToManyField

admin.site.register(Booking)
admin.site.register(Client)
admin.site.register(Admin)