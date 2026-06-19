from django.contrib import admin
from .models import Shipment, ShipmentHistory

class ShipmentHistoryInline(admin.TabularInline):
    model = ShipmentHistory
    extra = 1
    readonly_fields = ('timestamp',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'full_name', 'email', 'status', 'current_location', 'updated_at']
    list_filter = ['status']
    search_fields = ['tracking_id', 'full_name', 'email']
    readonly_fields = ['tracking_id', 'created_at', 'updated_at']
    inlines = [ShipmentHistoryInline]

    fieldsets = [
        ('Customer Information', {
            'fields': ('tracking_id', 'full_name', 'email', 'phone')
        }),
        ('Shipment Details', {
            'fields': ('origin', 'destination', 'shipping_address', 'loading_date')
        }),
        ('Tracking Status', {
            'fields': ('status', 'current_location', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]