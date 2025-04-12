// Cart functionality for ServiceStore

// Initialize cart in session if it doesn't exist
function initCart() {
    if (!sessionStorage.getItem('cart')) {
        sessionStorage.setItem('cart', JSON.stringify({}));
    }
}

// Add item to cart
function addToCart(serviceId, quantity = 1) {
    initCart();
    
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
}

// Update server-side cart
function updateServerCart(cart) {
    fetch('/orders/update_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ cart: cart })
    })
    .then(response => response.json())
    .then(data => {
        // Update cart icon with unique items count instead of total quantity
        const uniqueItemsCount = Object.keys(cart).length;
        updateCartIcon(uniqueItemsCount);
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
    
    // Set message and show notification
    notification.textContent = message;
    notification.classList.add('show');
    
    // Hide notification after 3 seconds and then remove it from DOM
    setTimeout(() => {
        notification.classList.remove('show');
        
        // Wait for the transition to complete before removing from DOM
        setTimeout(() => {
            if (notification && notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300); // Match the transition duration from CSS (0.3s)
    }, 3000);
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
        
        // Update badge content and visibility
        if (totalItems > 0 && !isCartPage) {
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
    
    // Get current cart
    let cart = JSON.parse(sessionStorage.getItem('cart'));
    
    // Update quantity based on action
    if (action === 'increase') {
        cart[serviceId] += 1;
    } else if (action === 'decrease') {
        if (cart[serviceId] > 1) {
            cart[serviceId] -= 1;
        }
    }
    
    // Save updated cart to session
    sessionStorage.setItem('cart', JSON.stringify(cart));
    
    // Update server-side session
    updateServerCart(cart);
    
    return cart[serviceId]; // Return new quantity
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

// Initialize cart when page loads and update cart icon
document.addEventListener('DOMContentLoaded', function() {
    initCart();
    
    // Get current cart and calculate unique items (number of keys in cart object)
    const cart = JSON.parse(sessionStorage.getItem('cart') || '{}');
    const uniqueItemsCount = Object.keys(cart).length;
    
    // Update cart icon with the unique items count
    updateCartIcon(uniqueItemsCount);
});