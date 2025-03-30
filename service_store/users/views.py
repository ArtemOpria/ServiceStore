from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def password_change(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успішно змінено!')
            return render(request, 'users/profile.html', {
                'form': profile_form,
                'password_change_form': form,
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
                            translated_errors.append('Ваш пароль занадто схожий на іншу особисту інформацію.')
                        elif "must contain at least 8" in error:
                            translated_errors.append('Ваш пароль повинен містити щонайменше 8 символів.')
                        elif "too common" in error:
                            translated_errors.append('Цей пароль занадто поширений.')
                        elif "entirely numeric" in error:
                            translated_errors.append('Ваш пароль не може складатися лише з цифр.')
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
    
    return render(request, 'users/profile.html', {
        'form': profile_form,
        'password_change_form': form,
        'active_tab': 'settings'  # Changed from 'password' to 'settings'
    })
