from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Category, ServiceImage


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ('image', 'title', 'order', 'thumbnail')
    readonly_fields = ('thumbnail',)
    
    def thumbnail(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'Перегляд'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_categories', 'price', 'view_gallery')
    list_filter = ('categories', 'price', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-price',)
    inlines = [ServiceImageInline]
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price', 'categories', 'image', 'is_active')
        }),
    )
    
    def view_gallery(self, obj):
        count = obj.gallery_images.count()
        if count:
            return format_html('<a href="{}?service__id__exact={}">{} зображень</a>', 
                              '/admin/services/serviceimage/', obj.id, count)
        return "Немає зображень"
    view_gallery.short_description = 'Галерея'
    
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'service', 'title', 'order')
    list_filter = ('service',)
    search_fields = ('service__name', 'title')
    ordering = ('service', 'order')
    raw_id_fields = ('service',)
    
    fieldsets = (
        ('Зображення', {
            'fields': ('service', 'image', 'title', 'order')
        }),
    )
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'Мініатюра'

admin.site.register(Service, ServiceAdmin)
admin.site.register(Category)
admin.site.register(ServiceImage, ServiceImageAdmin)
