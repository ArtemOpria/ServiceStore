from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class AdminAuthenticationForm(AuthenticationForm):
    """
    Форма аутентифікації для адмін-панелі з українськими повідомленнями про помилки.
    """
    username = forms.CharField(
        label='Ім\'я адміністратора',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        error_messages={
            'required': 'Це поле обов\'язкове.',
            'invalid': 'Введіть коректне ім\'я адміністратора.'
        }
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )

    error_messages = {
        'invalid_login': 'Будь ласка, введіть правильне ім\'я адміністратора та пароль',
        'inactive': 'Цей обліковий запис неактивний.'
    }