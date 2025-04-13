from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order
from services.models import Service


def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


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
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }
    
    return render(request, 'orders/cart.html', context)


@login_required
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
    
    if request.method == 'POST':
        # Process the checkout form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        payment_method = request.POST.get('payment_method')
        
        # Create orders for each item in the cart
        if cart_items:
            for item in cart_items:
                order = Order(
                    user=request.user,
                    service=item['service'],
                    total_price=item['total_price']
                )
                order.save()
            
            # Send confirmation email
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            
            subject = 'Підтвердження замовлення'
            html_message = render_to_string('orders/email/order_confirmation.html', {
                'user': request.user,
                'cart_items': cart_items,
                'total': total,
                'first_name': first_name,
                'last_name': last_name
            })
            plain_message = strip_tags(html_message)
            from_email = 'noreply@servicestore.com'
            to_email = email
            
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            
            # Clear the cart
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            
            # Redirect to order list with success message
            from django.contrib import messages
            messages.success(request, 'Ваше замовлення успішно оформлено! Підтвердження надіслано на вашу електронну пошту.')
            return redirect('order_list')
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }
    
    return render(request, 'orders/checkout.html', context)
