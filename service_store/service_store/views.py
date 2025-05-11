from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_subject = f"Контактна форма: {subject if subject else 'Без теми'}"
        email_message = f"Ім'я: {name}\nEmail: {email}\n\nПовідомлення:\n{message}"
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER], 
                fail_silently=False,
            )
            messages.success(request, 'Ваше повідомлення успішно надіслано! Ми зв\'яжемося з вами найближчим часом.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'Виникла помилка при відправці повідомлення. Будь ласка, спробуйте пізніше.')
    
    return render(request, 'contact.html')
