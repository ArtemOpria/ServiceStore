from django import template
import os
from django.conf import settings

register = template.Library()

@register.filter
def file_exists(file_path):
    """
    Перевіряє, чи існує файл фізично на сервері.
    Використання: {{ service.image.url|file_exists }}
    """
    if not file_path:
        return False
    
    if file_path.startswith(settings.MEDIA_URL):
        relative_path = file_path[len(settings.MEDIA_URL):]
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        return os.path.exists(absolute_path)
    
    if file_path.startswith(settings.STATIC_URL):
        relative_path = file_path[len(settings.STATIC_URL):]
        for static_dir in settings.STATICFILES_DIRS:
            absolute_path = os.path.join(static_dir, relative_path)
            if os.path.exists(absolute_path):
                return True
        return False
    
    return os.path.exists(file_path)
