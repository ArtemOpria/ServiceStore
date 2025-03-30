from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'service__name')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'service', 'total_price')
        }),
        ('Status Information', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('order_date',)

admin.site.register(Order, OrderAdmin)
