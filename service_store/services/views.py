from django.shortcuts import render, get_object_or_404

from .models import Service


def service_list(request):
    services = Service.objects.all()
    
    # Сортування
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price':
        services = services.order_by('price')
    elif sort_by == 'popularity':
        # Тут можна додати логіку сортування за популярністю
        # Наприклад, якщо б у моделі було поле для відстеження переглядів
        pass
    
    # Пагінація
    items_per_page = request.GET.get('items_per_page', 16)
    try:
        items_per_page = int(items_per_page)
        if items_per_page not in [16, 32, 48]:
            items_per_page = 16
    except ValueError:
        items_per_page = 16
    
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
    }
    
    return render(request, 'services/service_list.html', context)


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'services/service_detail.html', {'service': service})
