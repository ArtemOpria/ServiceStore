from django.contrib import admin
from .models import Service, Category

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_categories', 'price')
    list_filter = ('categories', 'price', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-price',)
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price', 'categories', 'image', 'is_active')
        }),
    )
    
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

admin.site.register(Service, ServiceAdmin)
admin.site.register(Category)
