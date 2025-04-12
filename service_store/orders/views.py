from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
    return render(request, 'orders/checkout.html', {'message': 'Сторінка оформлення замовлення в розробці'})
