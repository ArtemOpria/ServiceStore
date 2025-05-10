document.addEventListener('DOMContentLoaded', function() {
    // Додаємо прямі обробники для кнопок редагування при завантаженні сторінки
    const editButtons = document.querySelectorAll('.edit-review-btn');
    console.log('Пошук кнопок редагування на сторінці...');
    if (editButtons.length > 0) {
        console.log('Знайдено кнопки редагування:', editButtons.length);
        editButtons.forEach(button => {
            console.log('Додаємо обробник для кнопки:', button);
            button.addEventListener('click', function(e) {
                e.preventDefault(); // Запобігаємо стандартній поведінці
                console.log('Пряме натискання на кнопку редагування');
                const reviewId = this.getAttribute('data-review-id');
                const rating = this.getAttribute('data-rating');
                const comment = this.getAttribute('data-comment');
                
                console.log('Дані для редагування:', { reviewId, rating, comment });
                
                // Показуємо форму редагування
                const reviewFormContainer = document.getElementById('review-form-container');
                if (reviewFormContainer) {
                    reviewFormContainer.style.display = 'block';
                    
                    // Приховуємо кнопку "Залишити відгук"
                    const showReviewFormBtn = document.getElementById('show-review-form-btn');
                    if (showReviewFormBtn) {
                        showReviewFormBtn.style.display = 'none';
                    }
                    
                    // Змінюємо заголовок форми
                    const formTitle = document.getElementById('review-form-title');
                    if (formTitle) {
                        formTitle.textContent = 'Редагувати відгук';
                    }
                    
                    // Заповнюємо форму поточними даними
                    const ratingSelect = document.getElementById('id_rating');
                    const commentTextarea = document.getElementById('id_comment');
                    
                    if (ratingSelect) {
                        ratingSelect.value = rating;
                        // Оновлюємо відображення зірок
                        if (window.setStars) {
                            window.setStars(rating);
                        }
                    }
                    
                    if (commentTextarea) {
                        commentTextarea.value = comment;
                    }
                    
                    // Змінюємо форму для редагування
                    const reviewForm = document.getElementById('review-form');
                    if (reviewForm) {
                        reviewForm.setAttribute('data-review-id', reviewId);
                        reviewForm.setAttribute('data-edit-mode', 'true');
                        
                        // Змінюємо текст кнопки
                        const submitButton = reviewForm.querySelector('button[type="submit"]');
                        if (submitButton) {
                            submitButton.textContent = 'Зберегти зміни';
                        }
                    }
                }
            });
        });
    }
    // Функціонал для галереї зображень
    const thumbnails = document.querySelectorAll('.gallery-thumbnail');
    const mainImage = document.getElementById('main-product-image');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Оновлення основного зображення
            mainImage.src = this.getAttribute('data-src');
            
            // Оновлення активного стану мініатюр
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Функціонал для повноекранного перегляду галереї
    const galleryImages = document.querySelectorAll('.gallery-image');
    const galleryModal = new bootstrap.Modal(document.getElementById('galleryModal'));
    const fullscreenImage = document.getElementById('fullscreen-image');
    const modalTitle = document.getElementById('galleryModalLabel');
    const prevButton = document.getElementById('prev-image');
    const nextButton = document.getElementById('next-image');
    
    let currentImageIndex = 0;
    const imagesData = [];
    
    // Збираємо дані про всі зображення галереї
    galleryImages.forEach((image, index) => {
        imagesData.push({
            id: image.getAttribute('data-image-id'),
            url: image.getAttribute('data-image-url'),
            title: image.getAttribute('data-image-title')
        });
        
        // Додаємо обробник кліку для відкриття модального вікна
        image.addEventListener('click', function() {
            currentImageIndex = index;
            showFullscreenImage(currentImageIndex);
            galleryModal.show();
        });
    });
    
    // Функція для відображення зображення у повноекранному режимі
    function showFullscreenImage(index) {
        if (imagesData.length === 0) return;
        
        const imageData = imagesData[index];
        fullscreenImage.src = imageData.url;
        modalTitle.textContent = imageData.title || 'Перегляд зображення';
    }
    
    // Обробники для кнопок навігації
    prevButton.addEventListener('click', function() {
        currentImageIndex = (currentImageIndex - 1 + imagesData.length) % imagesData.length;
        showFullscreenImage(currentImageIndex);
    });
    
    nextButton.addEventListener('click', function() {
        currentImageIndex = (currentImageIndex + 1) % imagesData.length;
        showFullscreenImage(currentImageIndex);
    });
    
    // Додаємо обробник клавіш для навігації
    document.addEventListener('keydown', function(e) {
        if (!document.getElementById('galleryModal').classList.contains('show')) return;
        
        if (e.key === 'ArrowLeft') {
            currentImageIndex = (currentImageIndex - 1 + imagesData.length) % imagesData.length;
            showFullscreenImage(currentImageIndex);
        } else if (e.key === 'ArrowRight') {
            currentImageIndex = (currentImageIndex + 1) % imagesData.length;
            showFullscreenImage(currentImageIndex);
        } else if (e.key === 'Escape') {
            galleryModal.hide();
        }
    });
    
    // Функціонал для кількості послуг
    const decreaseBtn = document.getElementById('decrease-quantity');
    const increaseBtn = document.getElementById('increase-quantity');
    const quantityInput = document.getElementById('quantity');
    
    // Ініціалізуємо змінну для відстеження кількості
    let quantity = 1;
    
    // Забороняємо введення тексту в поле кількості
    if (quantityInput) {
        quantityInput.addEventListener('keydown', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Встановлюємо початкове значення з поля вводу
        quantity = parseInt(quantityInput.value);
        
        // Оновлюємо змінну quantity при зміні значення в полі
        quantityInput.addEventListener('change', function() {
            quantity = parseInt(this.value);
        });
    }
    
    if (decreaseBtn) {
        decreaseBtn.addEventListener('click', function() {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
                // Оновлюємо змінну quantity
                quantity = currentValue - 1;
            }
        });
    }
    
    if (increaseBtn) {
        increaseBtn.addEventListener('click', function() {
            const currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
            // Оновлюємо змінну quantity
            quantity = currentValue + 1;
        });
    }
    
    // Ініціалізація табів Bootstrap
    const tabEl = document.querySelector('button[data-bs-toggle="tab"]');
    tabEl && new bootstrap.Tab(tabEl);
    
    // Get the add to cart button
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    
    // Add event listener for add to cart button
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            const serviceId = this.getAttribute('data-service-id');
            // Отримуємо поточне значення кількості з поля вводу
            const currentQuantity = parseInt(quantityInput.value) || 1;
            // Call the addToCart function from cart.js з поточною кількістю
            addToCart(serviceId, currentQuantity);
        });
    }
    
    // Показ форми відгуку при натисканні на кнопку
    const showReviewFormBtn = document.getElementById('show-review-form-btn');
    const reviewFormContainer = document.getElementById('review-form-container');
    
    if (showReviewFormBtn && reviewFormContainer) {
        showReviewFormBtn.addEventListener('click', function() {
            reviewFormContainer.style.display = 'block';
            showReviewFormBtn.style.display = 'none';
            // Скидаємо форму на випадок, якщо вона була використана для редагування
            const reviewForm = document.getElementById('review-form');
            if (reviewForm) {
                reviewForm.reset();
                reviewForm.removeAttribute('data-edit-mode');
                reviewForm.removeAttribute('data-review-id');
                
                // Повертаємо оригінальний текст кнопки
                const submitButton = reviewForm.querySelector('button[type="submit"]');
                if (submitButton) submitButton.textContent = 'Опублікувати';
                
                // Встановлюємо заголовок форми для нового відгуку
                const formTitle = document.getElementById('review-form-title');
                if (formTitle) {
                    formTitle.textContent = 'Залишити відгук';
                }
            }
        });
    }
    
    // Додаємо делегування подій для кнопок редагування як резервний варіант
    document.body.addEventListener('click', function(event) {
        // Перевіряємо, чи клікнуто на кнопку редагування або її дочірній елемент
        if (event.target.classList.contains('edit-review-btn') || event.target.closest('.edit-review-btn')) {
            event.preventDefault(); // Запобігаємо стандартній поведінці
            event.stopPropagation(); // Зупиняємо подальше розповсюдження події
            
            console.log('Клік на кнопку редагування через делегування');
            
            const button = event.target.classList.contains('edit-review-btn') ? 
                          event.target : 
                          event.target.closest('.edit-review-btn');
            
            const reviewId = button.getAttribute('data-review-id');
            const rating = button.getAttribute('data-rating');
            const comment = button.getAttribute('data-comment');
            
            console.log('Дані для редагування через делегування:', { reviewId, rating, comment });
            
            // Показуємо форму редагування
            const reviewFormContainer = document.getElementById('review-form-container');
            if (reviewFormContainer) {
                reviewFormContainer.style.display = 'block';
                
                // Приховуємо кнопку "Залишити відгук"
                const showReviewFormBtn = document.getElementById('show-review-form-btn');
                if (showReviewFormBtn) {
                    showReviewFormBtn.style.display = 'none';
                }
                
                // Змінюємо заголовок форми
                const formTitle = document.getElementById('review-form-title');
                if (formTitle) {
                    formTitle.textContent = 'Редагувати відгук';
                }
                
                // Заповнюємо форму поточними даними
                const ratingSelect = document.getElementById('id_rating');
                const commentTextarea = document.getElementById('id_comment');
                
                if (ratingSelect) {
                    ratingSelect.value = rating;
                    // Оновлюємо відображення зірок
                    if (window.setStars) {
                        window.setStars(rating);
                    }
                }
                
                if (commentTextarea) {
                    commentTextarea.value = comment;
                }
                
                // Змінюємо форму для редагування
                const reviewForm = document.getElementById('review-form');
                if (reviewForm) {
                    reviewForm.setAttribute('data-review-id', reviewId);
                    reviewForm.setAttribute('data-edit-mode', 'true');
                    
                    // Змінюємо текст кнопки
                    const submitButton = reviewForm.querySelector('button[type="submit"]');
                    if (submitButton) {
                        submitButton.textContent = 'Зберегти зміни';
                    }
                }
            }
        }
    });

    
    // Функціонал для видалення відгуків - використовуємо делегування подій
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-review-btn') || 
            event.target.closest('.delete-review-btn')) {
            
            const button = event.target.classList.contains('delete-review-btn') ? 
                          event.target : 
                          event.target.closest('.delete-review-btn');
            
            if (confirm('Ви впевнені, що хочете видалити цей відгук?')) {
                const reviewId = button.getAttribute('data-review-id');
                // Отримуємо ID послуги з URL або з атрибуту кнопки
                let serviceId = button.getAttribute('data-service-id');
                if (!serviceId) {
                    const pathParts = window.location.pathname.split('/');
                    serviceId = pathParts[pathParts.length - 2]; // Передостанній елемент шляху
                }
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                console.log('Видалення відгуку:', { reviewId, serviceId });
                
                fetch(`/services/${serviceId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        action: 'delete_review',
                        review_id: reviewId
                    })
                })
                .then(response => {
                    if (response.ok) {
                        // Видаляємо елемент відгуку з DOM
                        const reviewItem = button.closest('.review-item');
                        if (reviewItem) reviewItem.remove();
                        
                        // Оновлюємо лічильник відгуків
                        const reviewsCount = document.querySelectorAll('.review-item').length;
                        const reviewsHeading = document.querySelector('.reviews-section h3');
                        if (reviewsHeading) {
                            reviewsHeading.textContent = `Відгуки клієнтів (${reviewsCount})`;
                        }
                        
                        // Показуємо повідомлення, якщо немає відгуків
                        if (reviewsCount === 0) {
                            const reviewsList = document.querySelector('.reviews-list');
                            if (reviewsList) {
                                reviewsList.innerHTML = `
                                    <div class="alert alert-light">
                                        <p class="mb-0">Поки що немає відгуків для цієї послуги. Будьте першим, хто залишить відгук!</p>
                                    </div>
                                `;
                            }
                        }
                    } else {
                        alert('Помилка при видаленні відгуку. Спробуйте ще раз.');
                    }
                })
                .catch(error => {
                    console.error('Помилка:', error);
                    alert('Помилка при видаленні відгуку. Спробуйте ще раз.');
                });
            }
        }
    });
    
    // Обробка відправки форми редагування відгуку
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Отримуємо ID послуги з атрибуту data-service-id форми або з URL
            let serviceId = this.getAttribute('data-service-id');
            if (!serviceId) {
                // Якщо атрибут не знайдено, спробуємо отримати з URL
                const pathParts = window.location.pathname.split('/');
                serviceId = pathParts[pathParts.length - 2]; // Передостанній елемент шляху
            }
            
            const isEditMode = this.getAttribute('data-edit-mode') === 'true';
            const reviewId = isEditMode ? this.getAttribute('data-review-id') : null;
            const rating = document.getElementById('id_rating').value;
            const comment = document.getElementById('id_comment').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            let url = `/services/${serviceId}/`;
            
            console.log('Відправляємо відгук:', {
                action: isEditMode ? 'edit_review' : 'add_review',
                service_id: serviceId,
                review_id: reviewId,
                rating: rating,
                comment: comment
            });
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: isEditMode ? 'edit_review' : 'add_review',
                    service_id: serviceId,
                    review_id: reviewId,
                    rating: rating,
                    comment: comment
                })
            })
            .then(response => {
                console.log('Статус відповіді:', response.status);
                return response.json().catch(e => {
                    console.error('Помилка при розборі JSON:', e);
                    return { status: 'error', message: 'Неправильний формат відповіді' };
                }).then(data => {
                    console.log('Відповідь сервера:', data);
                    if (data.status === 'success' || response.ok) {
                        // Перезавантажуємо сторінку для відображення змін
                        window.location.reload();
                    } else {
                        const errorMsg = data.errors ? JSON.stringify(data.errors) : (data.message || 'Спробуйте ще раз.');
                        alert('Помилка при збереженні відгуку: ' + errorMsg);
                    }
                });
            })
            .catch(error => {
                console.error('Помилка:', error);
                alert('Помилка при збереженні відгуку. Спробуйте ще раз.');
            });
        });
        
        // Обробка кнопки скасування
        const cancelButton = document.getElementById('cancel-review-btn');
        if (cancelButton) {
            cancelButton.addEventListener('click', function() {
                // Приховуємо форму
                const reviewFormContainer = document.getElementById('review-form-container');
                if (reviewFormContainer) {
                    reviewFormContainer.style.display = 'none';
                    const showReviewFormBtn = document.getElementById('show-review-form-btn');
                    if (showReviewFormBtn) {
                        showReviewFormBtn.style.display = 'inline-block';
                    }
                }
                
                // Скидаємо форму
                reviewForm.reset();
                reviewForm.removeAttribute('data-edit-mode');
                reviewForm.removeAttribute('data-review-id');
                
                // Повертаємо оригінальний текст кнопки
                const submitButton = reviewForm.querySelector('button[type="submit"]');
                if (submitButton) submitButton.textContent = 'Опублікувати';
                
                // Повертаємо оригінальний заголовок форми
                const formTitle = document.getElementById('review-form-title');
                if (formTitle) {
                    formTitle.textContent = 'Залишити відгук';
                }
            });
        }
    }

    const stars = document.querySelectorAll('#star-rating i');
    const ratingInput = document.getElementById('id_rating');

    // Робимо функцію setStars глобальною, щоб вона була доступна при редагуванні відгуку
    window.setStars = function(rating) {
        const stars = document.querySelectorAll('#star-rating i');
        stars.forEach(star => {
            const value = star.getAttribute('data-value');
            if (value <= rating) {
                star.classList.remove('far');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    };
    
    // Локальна функція для використання в цьому контексті
    function setStars(rating) {
        window.setStars(rating);
    }

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const rating = star.getAttribute('data-value');
            ratingInput.value = rating;
            setStars(rating);
        });

        star.addEventListener('mouseover', () => {
            const hoverRating = star.getAttribute('data-value');
            setStars(hoverRating);
        });

        star.addEventListener('mouseout', () => {
            setStars(ratingInput.value);
        });
    });

    // Initialize stars based on current value
    setStars(ratingInput.value);

});