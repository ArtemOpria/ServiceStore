from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from services.models import Service, Category
import uuid
import random
import string
from django.utils import timezone


class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Номер замовлення', blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID замовлення')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Користувач')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Загальна сума')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'В очікуванні'),
        ('in_progress', 'В процесі'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    ], default='pending', verbose_name='Статус')

    first_name = models.CharField(max_length=100, blank=True, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Прізвище')
    email = models.EmailField(blank=True, verbose_name='Електронна пошта')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адреса')
    city = models.CharField(max_length=100, blank=True, verbose_name='Місто')
    zip_code = models.CharField(max_length=20, blank=True, verbose_name='Поштовий індекс')
    
    delivery_method = models.CharField(max_length=20, choices=[
        ('nova_poshta', 'Нова Пошта'),
        ('ukr_poshta', 'Укрпошта'),
        ('courier', 'Кур\'єрська доставка'),
    ], blank=True, verbose_name='Спосіб доставки')
    payment_method = models.CharField(max_length=20, choices=[
        ('googlepay', 'Google Pay'),
        ('cash_on_delivery', 'Оплата під час отримання'),
    ], blank=True, verbose_name='Спосіб оплати')
    
    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.order_number}"
        
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{date_str}-{random_str}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Замовлення')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Послуга')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна за одиницю')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Підсумок')
    
    class Meta:
        verbose_name = 'Послуга в замовленні'
        verbose_name_plural = 'Склад замовлення'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.service.name} in Order {self.order.order_number}"
