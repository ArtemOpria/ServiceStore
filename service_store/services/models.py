from django.db import models
import os

def service_image_path(instance, filename):
    # Генеруємо шлях для збереження зображення: media/services/<filename>
    return os.path.join('services', filename)
    
def service_gallery_path(instance, filename):
    # Генеруємо шлях для збереження зображень галереї: media/services/gallery/<service_id>/<filename>
    return os.path.join('services', 'gallery', str(instance.service.id), filename)

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Назва')
    description = models.TextField(blank=True, null=True, verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    categories = models.ManyToManyField(Category, related_name='services', blank=True, verbose_name='Категорії')
    image = models.ImageField(upload_to=service_image_path, null=True, blank=True, verbose_name='Зображення')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_services', blank=True, verbose_name='У списку бажань')
    
    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        
    # Вкладки для адмін-панелі
    class Admin:
        fieldsets = [
            ('Інформація про послугу', {'fields': ['name', 'description', 'price', 'image', 'is_active']}),
            ('Загальне', {'fields': ['categories']}),
            ('Деталі відгуків', {'fields': ['favorited_by']}),
            ('Дати', {'fields': ['created_at', 'updated_at']}),
        ]

    def __str__(self):
        return self.name
        
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return total_rating / reviews.count()
        return 0
        
    def get_gallery_images(self):
        """Повертає всі зображення галереї для цієї послуги"""
        return self.gallery_images.all()


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Користувач')
    service = models.ForeignKey(Service, related_name='reviews', on_delete=models.CASCADE, verbose_name='Послуга')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        unique_together = ('user', 'service')
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

    def __str__(self):
        return f"Review by {self.user.username} for {self.service.name}"


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='gallery_images', on_delete=models.CASCADE, verbose_name='Послуга')
    image = models.ImageField(upload_to=service_gallery_path, verbose_name='Зображення')
    title = models.CharField(max_length=255, blank=True, verbose_name='Назва')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Зображення послуги'
        verbose_name_plural = 'Зображення послуги'
    
    def __str__(self):
        return f"Зображення для {self.service.name} #{self.order}"
