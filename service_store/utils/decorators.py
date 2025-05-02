from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def login_required_with_message(message, redirect_to='login'):
    """
    Декоратор, який перевіряє, чи користувач авторизований.
    Якщо ні, додає повідомлення та перенаправляє на сторінку входу.
    Для AJAX-запитів повертає відповідний HTTP-статус.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, message)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    from django.urls import reverse
                    response = JsonResponse({'status': 'error', 'message': message})
                    response.status_code = 302
                    response['Location'] = reverse(redirect_to) if not redirect_to.startswith('/') else redirect_to
                    return response
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator