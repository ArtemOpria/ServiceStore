document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.auth-form');

    forms.forEach(form => {
        const fields = form.querySelectorAll('.form-control');

        // Додаємо обробники подій для кожного поля
        fields.forEach(field => {
            field.addEventListener('input', function() {
                validateField(this);
            });

            field.addEventListener('blur', function() {
                validateField(this);
            });
        });

        // Валідація при відправці форми
        form.addEventListener('submit', function(event) {
            let isValid = true;

            fields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });

            // Перевірка паролів при реєстрації
            const password1 = form.querySelector('[name="password1"]');
            const password2 = form.querySelector('[name="password2"]');
            if (password1 && password2 && password1.value !== password2.value) {
                showError(password2, 'Паролі не співпадають');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;

        // Очищаємо попередні помилки
        field.classList.remove('is-invalid');
        const errorDiv = field.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }

        // Перевірка обов'язкових полів
        if (field.required && !value) {
            showError(field, 'Це поле обов\'язкове');
            isValid = false;
        }

        // Перевірка email
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                showError(field, 'Введіть коректну електронну адресу');
                isValid = false;
            }
        }

        // Перевірка паролю
        if (field.type === 'password' && value) {
            if (value.length < 8) {
                showError(field, 'Пароль повинен містити мінімум 8 символів');
                isValid = false;
            }
        }

        return isValid;
    }

    function showError(field, message) {
        field.classList.add('is-invalid');
        let errorDiv = field.parentElement.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            field.parentElement.insertBefore(errorDiv, field.nextSibling);
        }

        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
});