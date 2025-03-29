from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'price')
    list_filter = ('date', 'location')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
    fieldsets = (
        ('Event Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Date and Location', {
            'fields': ('date', 'location')
        }),
    )

admin.site.register(Event, EventAdmin)
