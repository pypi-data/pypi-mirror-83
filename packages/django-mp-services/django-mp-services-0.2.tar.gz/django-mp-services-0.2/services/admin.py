
from django.contrib import admin

from services.models import Service, ServiceItem, ServiceCategory


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = ['id', 'created', 'customer', 'item', 'price']


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):

    search_fields = ['name', 'code']
    list_display = ['id', 'name', 'code', 'price']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_display = ['id', 'name']
