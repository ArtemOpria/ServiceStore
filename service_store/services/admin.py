from django.contrib import admin
from .models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'price')
    list_filter = ('date', 'price')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price')
        }),
    )

admin.site.register(Service, ServiceAdmin)
