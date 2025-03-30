from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'event__name')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'event', 'total_price')
        }),
        ('Status Information', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('order_date',)

admin.site.register(Order, OrderAdmin)
