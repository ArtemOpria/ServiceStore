from django.contrib import admin
from django.contrib.admin import AdminSite
from users.admin_forms import AdminAuthenticationForm

# Налаштування адміністративної панелі з українськими повідомленнями про помилки
admin.site.login_form = AdminAuthenticationForm
admin.site.login_template = 'admin/login.html'

# Змінюємо заголовки адмін-панелі українською
admin.site.site_header = 'Адміністрування Floral Charm'
admin.site.site_title = 'Адмін-панель'
admin.site.index_title = 'Панель керування'