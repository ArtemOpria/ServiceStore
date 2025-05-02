from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse

from .models import Service, Category, Review
from utils.decorators import login_required_with_message

@login_required_with_message(message="Для перегляду списку бажань необхідно увійти в акаунт.")
def favorites(request):
    favorite_services = request.user.favorite_services.all()
    return render(request, 'services/favorites.html', {
        'favorite_services': favorite_services
    })


def search_services(request):
    query = request.GET.get('query', '')
    services = Service.objects.all()
    
    if query:
        services = services.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    
    categories = Category.objects.all()
    
    context = {
        'services': services,
        'categories': categories,
        'query': query,
        'total_services': services.count(),
    }
    
    return render(request, 'services/search_results.html', context)


def service_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()
    
    # Фільтрація за категоріями
    category_ids = request.GET.getlist('category')
    if category_ids:
        services = services.filter(categories__id__in=category_ids).distinct()
    
    # Сортування
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price_asc':
        services = services.order_by('price')
    elif sort_by == 'price_desc':
        services = services.order_by('-price')
    
    # Пагінація
    items_per_page = request.GET.get('items_per_page', 9)
    try:
        items_per_page = int(items_per_page)
        if items_per_page not in [9, 18, 30]:
            items_per_page = 9
    except ValueError:
        items_per_page = 9
    
    page = request.GET.get('page', 1)
    try:
        page = int(page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    # Розрахунок індексів для слайсингу
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    # Загальна кількість елементів та сторінок
    total_services = services.count()
    total_pages = (total_services + items_per_page - 1) // items_per_page
    
    # Слайсинг подій для поточної сторінки
    services_page = services[start_index:end_index]
    
    # Створення списку сторінок для пагінації
    # Показуємо максимум 5 сторінок навколо поточної
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)
    
    context = {
        'services': services_page,
        'current_page': page,
        'total_pages': total_pages,
        'page_range': page_range,
        'items_per_page': items_per_page,
        'sort_by': sort_by,
        'categories': categories,
        'total_services': total_services,
    }
    
    return render(request, 'services/service_list.html', context)


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = service.reviews.all().order_by('-created_at')
    review_form = None
    user_review = None
    
    if request.user.is_authenticated:
        try:
            user_review = reviews.get(user=request.user)
        except Review.DoesNotExist:
            from .forms import ReviewForm
            review_form = ReviewForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        from .forms import ReviewForm
        if user_review:
            review_form = ReviewForm(request.POST, instance=user_review)
        else:
            review_form = ReviewForm(request.POST)
            
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': review_form.errors})
    
    context = {
        'service': service,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'reviews_count': reviews.count()
    }
    
    return render(request, 'services/service_detail.html', context)


@login_required_with_message(message="Для додавання послуги до списку бажань необхідно увійти в акаунт.")
def toggle_favorite(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    user = request.user
    
    if service in user.favorite_services.all():
        user.favorite_services.remove(service)
        is_favorite = False
    else:
        user.favorite_services.add(service)
        is_favorite = True
    
    # Get the count of favorite services for the user
    favorite_count = user.favorite_services.count()
    
    return JsonResponse({
        'status': 'success',
        'is_favorite': is_favorite,
        'favorite_count': favorite_count
    })


def check_auth_for_cart(request, service_id):
    """
    Перевіряє авторизацію користувача для додавання товару до кошика.
    Якщо користувач не авторизований, перенаправляє на сторінку входу.
    """
    if not request.user.is_authenticated:
        login_url = reverse('login') + '?next=' + request.META.get('HTTP_REFERER', '/')
        return JsonResponse({
            'status': 'redirect',
            'redirect_url': login_url,
            'message': "Для додавання товару до кошика необхідно увійти в акаунт."
        })
    
    # Якщо користувач авторизований, повертаємо успішну відповідь
    return JsonResponse({
        'status': 'success',
        'is_authenticated': True
    })
