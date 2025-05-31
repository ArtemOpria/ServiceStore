from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class AdminAuthenticationForm(AuthenticationForm):
    """
    Форма аутентифікації для адмін-панелі з українськими повідомленнями про помилки.
    """
    username = forms.CharField(
        label='Електронна пошта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        error_messages={
            'required': 'Це поле обов\'язкове.',
            'invalid': 'Введіть коректну електронну пошту'
        }
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )

    error_messages = {
        'invalid_login': 'Будь ласка, перевірте дані входу та спробуйте ще раз.',
        'inactive': 'Цей обліковий запис неактивний.'
    }
