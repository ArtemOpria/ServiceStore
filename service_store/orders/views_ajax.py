from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from services.models import Service

@require_POST
@csrf_exempt
def update_cart(request):
    """Update the cart in the session"""
    try:
        data = json.loads(request.body)
        cart_data = data.get('cart', {})
        
        request.session['cart'] = cart_data
        request.session.modified = True
        
        total_items = sum(cart_data.values())
        
        return JsonResponse({
            'status': 'success',
            'total_items': total_items
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)