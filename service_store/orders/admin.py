from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'uuid', 'user', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'uuid', 'user__email', 'first_name', 'last_name', 'email', 'phone')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Інформація про замовлення', {
            'fields': ('order_number', 'uuid', 'user', 'total_price', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Інформація про доставку', {
            'fields': ('address', 'city', 'zip_code', 'delivery_method', 'payment_method')
        }),
        ('Інформація про статус', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('order_date', 'order_number', 'uuid')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'service__name')

admin.site.register(Order, OrderAdmin)
