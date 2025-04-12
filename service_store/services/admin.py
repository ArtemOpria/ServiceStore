from django.contrib import admin
from .models import Service, Category

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    ordering = ('-price',)
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price', 'category', 'image', 'is_active')
        }),
    )

admin.site.register(Service, ServiceAdmin)
admin.site.register(Category)
