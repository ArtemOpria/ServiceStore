from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Електронна пошта',
        error_messages={
            'required': 'Це поле обов\'язкове.',
            'invalid': 'Введіть коректну електронну адресу.'
        }
    )
    first_name = forms.CharField(
        label="Ім'я",
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    last_name = forms.CharField(
        label='Прізвище',
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Це поле обов\'язкове.',
            'password_too_short': 'Пароль занадто короткий. Він повинен містити принаймні 8 символів.',
            'password_too_common': 'Цей пароль занадто поширений.',
            'password_entirely_numeric': 'Пароль не може складатися тільки з цифр.',
            'password_too_similar': 'Пароль занадто схожий на ваше прізвище.'
        }
    )
    password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Це поле обов\'язкове.',
        }
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Паролі не співпадають.'))

        return password2

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Це поле обов\'язкове.',
            'invalid': 'Введіть коректну електронну адресу.'
        }
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )

    error_messages = {
        'invalid_login': 'Елекронна пошта або пароль введено невірно',
        'inactive': 'Цей обліковий запис неактивний.'
    }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Зберігаємо зміни в полях користувача
            if 'first_name' in self.cleaned_data and 'last_name' in self.cleaned_data:
                user = profile.user
                user.first_name = self.cleaned_data['first_name']
                user.last_name = self.cleaned_data['last_name']
                user.save()
            profile.save()
        return profile
