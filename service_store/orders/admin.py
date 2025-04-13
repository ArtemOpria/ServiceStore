from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username',)
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'total_price')
        }),
        ('Status Information', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('order_date',)

admin.site.register(Order, OrderAdmin)
