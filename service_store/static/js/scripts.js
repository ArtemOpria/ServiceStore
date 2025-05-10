document.addEventListener('DOMContentLoaded', function () {
    // Функціональність для перемикання режиму відображення (сітка/список)
    const gridViewBtn = document.getElementById('grid-view');
    const listViewBtn = document.getElementById('list-view');
    const productsContainer = document.getElementById('products-container');
    const filterForm = document.getElementById('filter-form');
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    const filterPopup = document.getElementById('filter-popup');
    const selectedFiltersCount = document.getElementById('selected-filters-count');
    const showResultsBtn = document.getElementById('show-results-btn');
    
    // Функція для збереження вибраних категорій в localStorage
    function saveSelectedCategories() {
        const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
        const selectedCategories = Array.from(categoryCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        localStorage.setItem('selectedCategories', JSON.stringify(selectedCategories));
    }
    
    // Функція для відновлення вибраних категорій з localStorage
    function restoreSelectedCategories() {
        const savedCategories = localStorage.getItem('selectedCategories');
        if (savedCategories) {
            const selectedCategories = JSON.parse(savedCategories);
            const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
            
            categoryCheckboxes.forEach(checkbox => {
                if (selectedCategories.includes(checkbox.value)) {
                    checkbox.checked = true;
                }
            });
        }
    }

    // Функція для збереження вибраного режиму відображення в localStorage
    function saveViewMode(mode) {
        localStorage.setItem('viewMode', mode);
    }

    // Функція для отримання збереженого режиму відображення
    function getViewMode() {
        return localStorage.getItem('viewMode') || 'grid';
    }

    // Функція для встановлення режиму відображення
    function setViewMode(mode) {
        if (mode === 'list') {
            productsContainer.classList.remove('products-grid');
            productsContainer.classList.add('products-list');
            gridViewBtn.classList.remove('active');
            listViewBtn.classList.add('active');
        } else {
            productsContainer.classList.remove('products-list');
            productsContainer.classList.add('products-grid');
            listViewBtn.classList.remove('active');
            gridViewBtn.classList.add('active');
        }
    }

    // Встановлення початкового режиму відображення
    setViewMode(getViewMode());

    // Обробники подій для кнопок перемикання режиму відображення
    gridViewBtn.addEventListener('click', function () {
        setViewMode('grid');
        saveViewMode('grid');
    });

    listViewBtn.addEventListener('click', function () {
        setViewMode('list');
        saveViewMode('list');
    });

    // Функція для підрахунку вибраних фільтрів та оновлення URL
    function updateSelectedFiltersCount() {
        const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
        const selectedCategories = Array.from(categoryCheckboxes).filter(cb => cb.checked);
        
        // Зберігаємо вибрані категорії в localStorage
        saveSelectedCategories();
        
        // Формуємо URL з вибраними категоріями
        const url = new URL(window.location.href);
        url.searchParams.delete('category');
        selectedCategories.forEach(checkbox => {
            url.searchParams.append('category', checkbox.value);
        });

        // Оновлюємо URL без перезавантаження сторінки
        window.history.pushState({}, '', url);

        // Відправляємо AJAX запит для отримання кількості послуг
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const totalServices = doc.getElementById('total-services').value;
                
                // Оновлюємо лічильник
                selectedFiltersCount.textContent = `Послуги: ${totalServices}`;
                
                // Toggle popup visibility if needed
                if (filterPopup) {
                    if (totalServices > 0) {
                        filterPopup.classList.add('active');
                    } else {
                        filterPopup.classList.remove('active');
                    }
                }
            });
    }

    // Функція для фіксації бокової панелі при прокручуванні
    function handleStickyFilterSidebar() {
        const filterSidebar = document.getElementById('filter-sidebar');
        const sidebarTop = filterSidebar.getBoundingClientRect().top;
        const scrollTop = window.scrollY;

        if (scrollTop > sidebarTop) {
            filterSidebar.classList.add('sticky');
        } else {
            filterSidebar.classList.remove('sticky');
        }
    }

    // Додавання обробника події прокручування для фіксації бокової панелі
    window.addEventListener('scroll', handleStickyFilterSidebar);

    // Додавання обробників подій для чекбоксів
    filterCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.name === 'category') {
                updateSelectedFiltersCount();
            } else if (this.name === 'sort' || this.name === 'items_per_page') {
                filterForm.submit();
            }
        });
    });

    // Обробник події для кнопки "Показати"
    showResultsBtn.addEventListener('click', function () {
        filterForm.submit();
    });

    // Відновлюємо вибрані категорії з localStorage
    restoreSelectedCategories();
    
    // Початкове оновлення лічильника вибраних фільтрів
    updateSelectedFiltersCount();
});

// Зберігаємо вибрані категорії перед перезавантаженням сторінки
window.addEventListener('beforeunload', function() {
    const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
    const selectedCategories = Array.from(categoryCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    localStorage.setItem('selectedCategories', JSON.stringify(selectedCategories));
});