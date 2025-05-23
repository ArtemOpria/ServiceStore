from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from services.models import Service
from utils.decorators import login_required_with_message
from django.http import Http404


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required_with_message(message="Для оплати замовлення необхідно увійти в акаунт.")
def payment(request):
    # Отримуємо ID замовлення з сесії
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, 'Замовлення не знайдено')
        return redirect('cart')
    
    try:
        # Отримуємо замовлення з бази даних
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Перевіряємо, чи метод оплати - Google Pay
        if order.payment_method != 'googlepay':
            messages.error(request, 'Неправильний метод оплати')
            return redirect('order_detail', order_id=order.id)
        
        # Очищаємо кошик в сесії
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
        
        # Відображаємо сторінку оплати
        return render(request, 'orders/payment.html', {'order': order})
    
    except Order.DoesNotExist:
        raise Http404('Замовлення не знайдено')


def cart(request):
    cart_items = []
    subtotal = 0
    total = 0
    
    if 'cart' in request.session:
        cart_data = request.session['cart']
        for item_id, quantity in cart_data.items():
            try:
                service = Service.objects.get(id=item_id)
                item_total = service.price * quantity
                cart_items.append({
                    'id': item_id,
                    'service': service,
                    'quantity': quantity,
                    'total_price': item_total
                })
                subtotal += item_total
            except Service.DoesNotExist:
                pass
        
        total = subtotal
    
    # Передаємо помилки форми в контекст, якщо вони є
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
        'form_errors': form_errors if 'form_errors' in locals() else {}
    }
    
    return render(request, 'orders/cart.html', context)


@login_required_with_message(message="Для оформлення замовлення необхідно увійти в акаунт.")
def checkout(request):
    cart_items = []
    subtotal = 0
    total = 0
    
    if 'cart' in request.session:
        cart_data = request.session['cart']
        for item_id, quantity in cart_data.items():
            try:
                service = Service.objects.get(id=item_id)
                item_total = service.price * quantity
                cart_items.append({
                    'id': item_id,
                    'service': service,
                    'quantity': quantity,
                    'total_price': item_total
                })
                subtotal += item_total
            except Service.DoesNotExist:
                pass
        
        total = subtotal
    
    # Якщо кошик порожній, перенаправляємо на сторінку кошика
    if not cart_items:
        messages.warning(request, 'Ваш кошик порожній. Додайте послуги перед оформленням замовлення.')
        return redirect('cart')
    
    # Отримуємо дані профілю користувача
    user_profile = None
    phone = ''
    address = ''
    city = ''
    zip_code = ''
    
    try:
        user_profile = request.user.profile
        phone = user_profile.phone_number
        address = user_profile.address
        city = user_profile.city
        zip_code = user_profile.zip_code
    except:
        pass
    
    if request.method == 'POST':
        # Валідація форми
        form_valid = True
        form_errors = {}
        
        # Отримання та валідація даних форми
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        zip_code = request.POST.get('zip', '').strip()
        delivery_method = request.POST.get('delivery_method', '')
        payment_method = request.POST.get('payment_method', '')
        save_info = 'save_info' in request.POST
        
        # Перевірка обов'язкових полів
        if not first_name:
            form_valid = False
            form_errors['first_name'] = 'Це поле обов\'язкове'
        
        if not last_name:
            form_valid = False
            form_errors['last_name'] = 'Це поле обов\'язкове'
        
        if not email:
            form_valid = False
            form_errors['email'] = 'Це поле обов\'язкове'
        elif '@' not in email:
            form_valid = False
            form_errors['email'] = 'Введіть коректну електронну адресу'
        
        if not phone:
            form_valid = False
            form_errors['phone'] = 'Це поле обов\'язкове'
        
        if not address:
            form_valid = False
            form_errors['address'] = 'Це поле обов\'язкове'
        
        if not city:
            form_valid = False
            form_errors['city'] = 'Це поле обов\'язкове'
        
        if not zip_code:
            form_valid = False
            form_errors['zip'] = 'Це поле обов\'язкове'
        
        if not delivery_method:
            form_valid = False
            form_errors['delivery_method'] = 'Оберіть спосіб доставки'
            
        if not payment_method:
            form_valid = False
            form_errors['payment_method'] = 'Оберіть спосіб оплати'
        
        # Якщо форма валідна, створюємо замовлення
        if form_valid and cart_items:
            order = Order(
                user=request.user,
                total_price=total,
                status='pending',
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                zip_code=zip_code,
                delivery_method=delivery_method,
                payment_method=payment_method
            )
            order.save()
            
            # Створюємо елементи замовлення
            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    service=item['service'],
                    quantity=item['quantity'],
                    unit_price=item['service'].price,
                    subtotal=item['total_price']
                )
                order_item.save()
            
            # Відправляємо підтвердження на електронну пошту
            subject = 'Підтвердження замовлення'
            html_message = render_to_string('orders/email/order_confirmation.html', {
                'user': request.user,
                'cart_items': cart_items,
                'total': total,
                'first_name': first_name,
                'last_name': last_name,
                'order': order,
                'address': address,
                'city': city,
                'zip_code': zip_code,
                'phone': phone
            })
            plain_message = strip_tags(html_message)
            from_email = 'noreply@servicestore.com'
            to_email = email

            if payment_method == 'googlepay':
                request.session['order_id'] = order.id
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                return redirect('payment')
            
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            
            if save_info:
                user = request.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                
                try:
                    profile = user.profile
                    profile.phone_number = phone
                    profile.address = address
                    profile.city = city
                    profile.zip_code = zip_code
                    profile.save()
                except:
                    from users.models import Profile
                    profile = Profile(user=user, phone_number=phone, address=address, city=city, zip_code=zip_code)
                    profile.save()
                
            messages.success(request, 'Ваше замовлення успішно оформлено! Підтвердження надіслано на вашу електронну пошту.')
            
            response = redirect('profile')
            response.set_cookie('active_tab', 'orders', max_age=30)
            return response
        else:
            for field, error in form_errors.items():
                messages.error(request, f'{error}')
        
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
        'user_phone': phone,
        'user_address': address,
        'user_city': city,
        'user_zip': zip_code,
        'form_errors': form_errors if 'form_errors' in locals() else {}
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required_with_message(message="Для повторного замовлення необхідно увійти в акаунт.")
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    new_cart = {}
    for item in order.items.all():
        new_cart[str(item.service.id)] = item.quantity
    
    request.session['cart'] = new_cart
    request.session.modified = True
    
    return redirect('cart')
