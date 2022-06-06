from django.contrib import admin

from inventory import models


@admin.register(models.Planes)
class PlanesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']
    list_filter = ['status']
    search_fields = ['name']


@admin.register(models.Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.Attendants)
class AttendantsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'plane_id']


@admin.register(models.Providers)
class ProvidersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'base']


@admin.register(models.Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ['id', 'plane_id', 'origin', 'destination']


@admin.register(models.Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


@admin.register(models.PlaneStock)
class PlaneStockAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'plane_id', 'product_id', 'quantity', 'maximum_quantity'
    ]


@admin.register(models.Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'attendant_id', 'providers', 'base', 'date', 'status'
    ]


@admin.register(models.OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product_id', 'order_id', 'quantity', 'fill_quantity'
    ]


@admin.register(models.Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'description']
