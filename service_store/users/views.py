from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import ProfileForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Profile, CustomUser
from functools import wraps


def user_role_required(view_func):
    """Декоратор для перевірки, що користувач має роль USER"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != CustomUser.USER:
            messages.warning(request, 'Ця сторінка доступна лише для звичайних користувачів')
            if request.user.role == CustomUser.ADMIN:
                return redirect('admin:index')
            elif request.user.role == CustomUser.MANAGER:
                return redirect('manager:index')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Реєстрація успішна! Ласкаво просимо!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # AuthenticationForm uses 'username' field for the identifier
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Перевірка ролі користувача - адміністратори та менеджери не можуть входити через цю форму
                if user.role in [CustomUser.ADMIN, CustomUser.MANAGER]:
                    messages.error(request, 'Для авторизації перейдіть на сторінку логіну адміністратора')
                    return redirect('login')
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Невірна електронна пошта або пароль')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@user_role_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль успішно оновлено!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    # Отримуємо замовлення користувача для вкладки історії замовлень
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    
    # Визначаємо активну вкладку (з URL-параметра або за замовчуванням)
    active_tab = request.GET.get('active_tab', 'personal')
    if active_tab not in ['personal', 'orders', 'settings']:
        active_tab = 'personal'

    return render(request, 'users/profile.html', {
        'form': form, 
        'orders': orders,
        'active_tab': active_tab
    })


@user_role_required
def password_change(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успішно змінено!')
            # Отримуємо замовлення користувача для вкладки історії замовлень
            from orders.models import Order
            orders = Order.objects.filter(user=request.user).order_by('-order_date')
            
            return render(request, 'users/profile.html', {
                'form': profile_form,
                'password_change_form': form,
                'orders': orders,
                'active_tab': 'settings'  # Changed from 'password' to 'settings'
            })
        else:
            if 'old_password' in form.errors:
                form.errors.pop('old_password')
                form.add_error('old_password', 'Поточний пароль введено неправильно.')
            if 'new_password2' in form.errors:
                if form.data['new_password1'] != form.data['new_password2']:
                    form.errors.pop('new_password2')
                    form.add_error('new_password2', 'Паролі не співпадають. Будь ласка, введіть однакові паролі.')
                else:
                    error_messages = form.errors.get('new_password2', [])
                    translated_errors = []
                    
                    for error in error_messages:
                        if "too similar to" in error:
                            translated_errors.append('Пароль занадто схожий на іншу особисту інформацію.')
                        elif "must contain at least 8" in error:
                            translated_errors.append('Пароль повинен містити щонайменше 8 символів.')
                        elif "too common" in error:
                            translated_errors.append('Пароль занадто поширений.')
                        elif "entirely numeric" in error:
                            translated_errors.append('Пароль не може складатися лише з цифр.')
                        else:
                            continue

                    if translated_errors:
                        form.errors.pop('new_password2')
                        form.add_error('new_password2', ' '.join(translated_errors))
                    else:
                        form.add_error('new_password2', 'Помилка у новому паролі. Перевірте вимоги до пароля.')
            else:
                form.add_error(None, 'Будь ласка, виправте помилки нижче.')
    else:
        form = PasswordChangeForm(request.user)
    
    # Отримуємо замовлення користувача для вкладки історії замовлень
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    
    return render(request, 'users/profile.html', {
        'form': profile_form,
        'password_change_form': form,
        'orders': orders,
        'active_tab': 'settings'  # Changed from 'password' to 'settings'
    })
