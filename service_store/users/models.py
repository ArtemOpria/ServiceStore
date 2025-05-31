from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Адміністратор'),
        (MANAGER, 'Менеджер'),
        (USER, 'Користувач'),
    ]
    
    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default=USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Користувач')
    phone_number = models.CharField(max_length=25, blank=True, verbose_name='Номер телефону')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адреса')
    city = models.CharField(max_length=100, blank=True, verbose_name='Місто')
    zip_code = models.CharField(max_length=20, blank=True, verbose_name='Поштовий індекс')
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg', blank=True, verbose_name='Фото профілю')
    
    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f"{self.user.email}'s Profile"
