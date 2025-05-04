// Cart functionality for ServiceStore

// Initialize cart in session if it doesn't exist
function initCart() {
    if (!sessionStorage.getItem('cart')) {
        sessionStorage.setItem('cart', JSON.stringify({}));
    }
}

// Check if user is authenticated
function isUserAuthenticated() {
    // Look for a specific cookie or element that indicates authentication
    // This is a simple check - you might need to adjust based on your authentication system
    return document.body.classList.contains('user-authenticated');
}

// Add item to cart
function addToCart(serviceId, quantity = 1) {
    initCart();
    
    // Спочатку перевіряємо авторизацію користувача
    fetch(`/services/check_auth_for_cart/${serviceId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'redirect') {
            // Показуємо повідомлення користувачу про необхідність авторизації
            showCartNotification(data.message);
            
            // Перенаправляємо на сторінку входу через 2 секунди
            setTimeout(() => {
                window.location.href = data.redirect_url;
            }, 2000);
            
            return;
        }
        
        // Якщо користувач авторизований, продовжуємо додавання товару до кошика
        // Get current cart
        let cart = JSON.parse(sessionStorage.getItem('cart'));
        
        // Add or update item in cart
        if (cart[serviceId]) {
            cart[serviceId] += quantity;
        } else {
            cart[serviceId] = quantity;
        }
        
        // Save updated cart to session
        sessionStorage.setItem('cart', JSON.stringify(cart));
        
        // Update server-side session
        updateServerCart(cart);
        
        // Show success message
        showCartNotification('Товар додано до кошика');
    })
    .catch(error => {
        console.error('Error checking authentication:', error);
        showCartNotification('Помилка при додаванні товару до кошика');
    });
}

// Update server-side cart
function updateServerCart(cart) {
    // Ensure cart data is properly formatted with numeric values
    const formattedCart = {};
    
    // Convert all cart values to integers
    for (const [key, value] of Object.entries(cart)) {
        formattedCart[key] = parseInt(value) || 0; // Default to 0 if parsing fails
    }
    
    fetch('/orders/update_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ cart: formattedCart })
    })
    .then(response => {
        // Перевіряємо, чи це перенаправлення (статус 302)
        if (response.status === 302) {
            // Отримуємо URL для перенаправлення
            const redirectUrl = response.headers.get('Location');
            
            // Показуємо повідомлення користувачу про необхідність авторизації
            showCartNotification('Для додавання товару до кошика необхідно увійти в акаунт.');
            
            // Перенаправляємо на сторінку входу через 2 секунди
            setTimeout(() => {
                window.location.href = redirectUrl || '/users/login/';
            }, 2000);
            
            // Повертаємо об'єкт з помилкою, щоб перервати ланцюжок then
            return { status: 'redirect' };
        }
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Пропускаємо обробку, якщо це було перенаправлення
        if (data.status === 'redirect') {
            return;
        }
        
        if (data.status === 'success') {
            // Update cart icon with unique items count
            const uniqueItemsCount = Object.keys(formattedCart).length;
            updateCartIcon(uniqueItemsCount);
        } else {
            console.error('Error updating cart:', data.message);
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    });
}

// Show notification when item is added to cart
function showCartNotification(message) {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('cart-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'cart-notification';
        notification.className = 'cart-notification';
        document.body.appendChild(notification);
    }
    
    // Очищаємо вміст повідомлення
    notification.innerHTML = '';
    
    // Створюємо контейнер для тексту
    const messageText = document.createElement('div');
    messageText.className = 'notification-message';
    messageText.textContent = message;
    notification.appendChild(messageText);
    
    // Додаємо кнопку переходу до кошика, якщо повідомлення про додавання товару
    if (message.includes('Товар додано до кошика')) {
        const goToCartButton = document.createElement('a');
        goToCartButton.href = '/orders/cart/';
        goToCartButton.className = 'go-to-cart-button';
        goToCartButton.innerHTML = '<i class="fas fa-shopping-cart"></i> Перейти до кошика';
        notification.appendChild(goToCartButton);
        
        // Додаємо стилі для кнопки, якщо вони ще не додані
        if (!document.getElementById('cart-notification-styles')) {
            const style = document.createElement('style');
            style.id = 'cart-notification-styles';
            style.textContent = `
                .cart-notification {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 10px;
                    padding: 15px;
                }
                .go-to-cart-button {
                    display: inline-flex;
                    align-items: center;
                    background-color:rgb(37, 94, 12);
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    text-decoration: none;
                    font-size: 14px;
                    margin-top: 5px;
                    transition: background-color 0.3s;
                }
                .go-to-cart-button:hover {
                    background-color:rgb(50, 90, 64);
                }
                .go-to-cart-button i {
                    margin-right: 5px;
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    notification.classList.add('show');
    
    // Hide notification after 4 seconds and then remove it from DOM
    setTimeout(() => {
        notification.classList.remove('show');
        
        // Wait for the transition to complete before removing from DOM
        setTimeout(() => {
            if (notification && notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Update cart icon with number of items
function updateCartIcon(totalItems) {
    const cartIcon = document.querySelector('.fa-shopping-cart');
    if (cartIcon) {
        // Find or create the badge element
        let badge = cartIcon.nextElementSibling;
        if (!badge || !badge.classList.contains('cart-badge')) {
            badge = document.createElement('span');
            badge.className = 'cart-badge';
            cartIcon.parentNode.appendChild(badge);
        }
        
        // Check if we're on the cart page
        const isCartPage = window.location.pathname.includes('/orders/cart/');
        
        // Only show cart badge if we have items AND
        // either we're authenticated OR we're on a page that should show the cart for anonymous users
        const shouldShowBadge = totalItems > 0 && !isCartPage && 
            (isUserAuthenticated() || window.location.pathname.includes('/services/'));
        
        // Update badge content and visibility
        if (shouldShowBadge) {
            badge.textContent = totalItems;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update item quantity in cart
function updateItemQuantity(serviceId, action) {
    initCart();
    
    // Ensure serviceId is a string
    serviceId = String(serviceId);
    
    // Get current cart
    let cart = JSON.parse(sessionStorage.getItem('cart'));
    
    // Ensure the item exists in cart
    if (!cart[serviceId]) {
        cart[serviceId] = 1;
    }
    
    // Update quantity based on action
    if (action === 'increase') {
        cart[serviceId] = parseInt(cart[serviceId]) + 1;
    } else if (action === 'decrease') {
        if (parseInt(cart[serviceId]) > 1) {
            cart[serviceId] = parseInt(cart[serviceId]) - 1;
        }
    }
    
    // Save updated cart to session
    sessionStorage.setItem('cart', JSON.stringify(cart));
    
    // Update server-side session
    updateServerCart(cart);
    
    return parseInt(cart[serviceId]); // Return new quantity as a number
}

// Remove item from cart
function removeItem(serviceId) {
    initCart();
    
    // Get current cart
    let cart = JSON.parse(sessionStorage.getItem('cart'));
    
    // Remove item from cart
    if (cart[serviceId]) {
        delete cart[serviceId];
    }
    
    // Save updated cart to session
    sessionStorage.setItem('cart', JSON.stringify(cart));
    
    // Update server-side session
    updateServerCart(cart);
    
    // Show notification
    showCartNotification('Товар видалено з кошика');
}

// Clear cart completely (used after checkout or when user manually clears cart)
function clearCart() {
    sessionStorage.setItem('cart', JSON.stringify({}));
    updateServerCart({});
    updateCartIcon(0);
    const isCartPage = window.location.pathname.includes('/orders/cart/');
    const message = isCartPage ? 'Кошик успішно очищено!' : 'Замовлення оформлено успішно!';
    showCartNotification(message);
}

// Initialize cart when page loads and update cart icon
document.addEventListener('DOMContentLoaded', function() {
    initCart();
    
    // Get current cart and calculate unique items (number of keys in cart object)
    const cart = JSON.parse(sessionStorage.getItem('cart') || '{}');
    const uniqueItemsCount = Object.keys(cart).length;
    
    // Перевіряємо, чи ми на сторінці профілю і чи є cookie для активації вкладки замовлень
    if (window.location.pathname.includes('/users/profile/')) {
        const activeTab = getCookie('active_tab');
        if (activeTab === 'orders') {
            // Активуємо вкладку замовлень
            setTimeout(() => {
                const ordersTab = document.getElementById('orders-tab');
                if (ordersTab) {
                    ordersTab.click();
                }
                // Видаляємо cookie після використання
                document.cookie = 'active_tab=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            }, 100);
            
            // Очищаємо кошик, якщо ми перейшли на профіль після оформлення замовлення
            clearCart();
        }
    }
    
    // Check if we need to sync with server cart (for authenticated users)
    // or clear cart (for users who just logged out)
    fetch('/orders/update_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ cart: cart, check_auth: true })
    })
    .then(response => {
        // Перевіряємо, чи це перенаправлення (статус 302)
        if (response.status === 302) {
            // Для перевірки автентифікації ми не перенаправляємо користувача,
            // а просто обробляємо як неавторизованого
            return response.json().then(() => {
                return { is_authenticated: false };
            }).catch(() => {
                return { is_authenticated: false };
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.is_authenticated) {
            // User is authenticated, update the body class
            document.body.classList.add('user-authenticated');
            
            // If server has a cart and we need to sync
            if (data.has_server_cart) {
                // Update local cart from server if needed
                sessionStorage.setItem('cart', JSON.stringify(data.cart || {}));
                updateCartIcon(Object.keys(data.cart || {}).length);
                return;
            }
        } else {
            // User is not authenticated, remove the body class
            document.body.classList.remove('user-authenticated');
            
            // If we're on a page where anonymous users shouldn't see cart items
            if (!window.location.pathname.includes('/services/')) {
                // Clear cart for anonymous users on non-service pages
                sessionStorage.setItem('cart', JSON.stringify({}));
                updateCartIcon(0);
                return;
            }
        }
        
        // Default: update cart icon with the unique items count
        updateCartIcon(uniqueItemsCount);
    })
    .catch(error => {
        console.error('Error checking authentication status:', error);
        // Fallback to default behavior
        updateCartIcon(uniqueItemsCount);
    });
});