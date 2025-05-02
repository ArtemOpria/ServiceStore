from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from services.models import Service
from utils.decorators import login_required_with_message

@require_POST
@csrf_exempt
@login_required_with_message(message="Для додавання товару до кошика необхідно увійти в акаунт.")
def update_cart(request):
    """Update the cart in the session and handle authentication checks"""
    try:
        data = json.loads(request.body)
        cart_data = data.get('cart', {})
        check_auth = data.get('check_auth', False)
        
        # Prepare response data
        response_data = {
            'status': 'success',
            'is_authenticated': request.user.is_authenticated
        }
        
        # If this is an authentication check request
        if check_auth:
            # Add authentication status to response
            if request.user.is_authenticated:
                # Check if user has items in their session cart
                has_server_cart = 'cart' in request.session and bool(request.session['cart'])
                response_data['has_server_cart'] = has_server_cart
                
                # If user has server cart, include it in the response
                if has_server_cart:
                    response_data['cart'] = request.session['cart']
            
            # For non-authenticated users or if not checking auth, just update the cart
            else:
                # Only update session for anonymous users if they're on service pages
                # This prevents cart persistence after logout
                request.session['cart'] = cart_data
                request.session.modified = True
        else:
            # Regular cart update (not an auth check)
            request.session['cart'] = cart_data
            request.session.modified = True
            
            # Include total items in response
            total_items = sum(cart_data.values())
            response_data['total_items'] = total_items
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)