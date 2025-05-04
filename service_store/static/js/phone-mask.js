document.addEventListener('DOMContentLoaded', function() {
    if (!window.IMask) {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/imask@6.4.3/dist/imask.min.js';
        script.async = true;
        script.onload = initPhoneMasks;
        document.head.appendChild(script);
    } else {
        initPhoneMasks();
    }

    function initPhoneMasks() {
        const phoneInputs = document.querySelectorAll('input[type="tel"], input[id="phone"]');
        
        phoneInputs.forEach(input => {
            const maskOptions = {
                mask: '+38 (000) 000-00-00',
                lazy: false,
                placeholderChar: '_'
            };
            
            const mask = IMask(input, maskOptions);
            
            // Clear on focus if empty
            input.addEventListener('focus', function() {
                if (mask.unmaskedValue === '') {
                    mask.value = '';
                }
            });
            
            // Clear on blur if incomplete
            input.addEventListener('blur', function() {
                if (mask.unmaskedValue.length < 10) {
                    mask.value = '';
                    input.value = '';
                }
            });
            
            // Add validation before form submission
            const form = input.closest('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    if (mask.unmaskedValue.length < 10) {
                        e.preventDefault();
                        input.classList.add('is-invalid');
                        input.nextElementSibling.textContent = 'Будь ласка, введіть повний номер телефону';
                        input.focus();
                    }
                });
            }
        });
    }
});