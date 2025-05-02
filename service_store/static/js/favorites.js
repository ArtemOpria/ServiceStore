function toggleFavorite(serviceId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const heartIcon = document.querySelector(`.favorite-btn[data-service-id="${serviceId}"] i`);
    const favoriteBtn = document.querySelector(`.favorite-btn[data-service-id="${serviceId}"]`);
    const favoriteText = favoriteBtn.querySelector('span');

    fetch(`/services/toggle-favorite/${serviceId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest' // Додаємо заголовок для ідентифікації AJAX-запиту
        },
        redirect: 'manual' // Змінюємо на 'manual', щоб самостійно обробити перенаправлення
    })
    .then(response => {
        // Перевіряємо статус відповіді
        if (response.status === 302 || response.type === 'opaqueredirect' || response.redirected) {
            // Перенаправляємо на сторінку логіну
            window.location.href = '/users/login/';
            return null;
        }
        // Якщо відповідь не є перенаправленням, обробляємо її як JSON
        if (!response.ok) {
            throw new Error('Помилка мережі або сервера');
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; // Якщо відбулося перенаправлення, data буде null
        if (data.status === 'success') {
            // Встановлюємо правильний клас залежно від стану обраного
            if (data.is_favorite) {
                heartIcon.classList.add('fas');
                heartIcon.classList.remove('far');
                favoriteBtn.classList.add('active');
                favoriteText && (favoriteText.textContent = 'Видалити з списку бажань');
            } else {
                heartIcon.classList.remove('fas');
                heartIcon.classList.add('far');
                favoriteBtn.classList.remove('active');
                favoriteText && (favoriteText.textContent = 'Додати до списку бажань');
            }

            // Оновлюємо лічильник обраного в навігації (якщо є)
            if (data.favorite_count !== undefined) {
                updateFavoriteCount(data.favorite_count);
            }

            // Якщо ми на сторінці обраного, видаляємо картку послуги
            if (window.location.pathname.includes('/favorites/') && !data.is_favorite) {
                const productCard = favoriteBtn.closest('.product-card');
                if (productCard) {
                    productCard.remove();
                    // Перевіряємо, чи залишились ще послуги
                    const remainingCards = document.querySelectorAll('.product-card');
                    if (remainingCards.length === 0) {
                        const productsContainer = document.getElementById('products-container');
                        productsContainer.innerHTML = '<div class="alert alert-info w-100 text-center">У вас поки немає збережених послуг</div>';
                    }
                }
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateFavoriteCount(count) {
    const favoriteCountElement = document.querySelector('.favorite-count');
    if (favoriteCountElement) {
        favoriteCountElement.textContent = count;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const serviceId = this.getAttribute('data-service-id');
            if (serviceId) {
                toggleFavorite(serviceId);
            }
        });
    });
});