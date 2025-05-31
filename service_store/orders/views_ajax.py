from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from services.models import Service
from utils.decorators import login_required_with_message

@require_POST
@csrf_exempt
@login_required_with_message(message="Для додавання послуги до кошика необхідно увійти в акаунт.")
def update_cart(request):
    """Update the cart in the session and handle authentication checks"""
    try:
        data = json.loads(request.body)
        action = data.get('action', None)
        
        response_data = {
            'status': 'success',
            'is_authenticated': request.user.is_authenticated
        }
        
        if action == 'clear':
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            response_data['cart_cleared'] = True
            return JsonResponse(response_data)
        
        cart_data = data.get('cart', {})
        check_auth = data.get('check_auth', False)
        
        if check_auth:
            if request.user.is_authenticated:
                has_server_cart = 'cart' in request.session and bool(request.session['cart'])
                response_data['has_server_cart'] = has_server_cart
                
                if has_server_cart:
                    response_data['cart'] = request.session['cart']
            
            else:
                request.session['cart'] = cart_data
                request.session.modified = True
        else:
            request.session['cart'] = cart_data
            request.session.modified = True
            
            total_items = sum(cart_data.values())
            response_data['total_items'] = total_items
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
