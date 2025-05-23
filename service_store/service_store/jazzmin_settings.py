# Налаштування Jazzmin для української локалізації

JAZZMIN_SETTINGS = {
    # Заголовок у вкладці браузера (за замовчуванням: 'Django')
    "site_title": "Floral Charm Адмін",

    # Заголовок на сторінці входу (за замовчуванням: 'Django Administration')
    "site_header": "Адміністрування Floral Charm",

    # Заголовок на головній сторінці адмін-панелі (за замовчуванням: 'Site Administration')
    "site_brand": "Floral Charm",

    # Заголовок на головній сторінці (за замовчуванням: 'Site administration')
    "welcome_sign": "Ласкаво просимо до адміністративної панелі Floral Charm",

    # Авторські права
    "copyright": "Floral Charm © 2023",
    
    # Відключення футера
    "show_footer": False,

    # Модель користувача (за замовчуванням: 'auth.User')
    "user_avatar": None,

    # Посилання на головну сторінку сайту
    "site_logo": "images/logo.png",

    # Іконки для додатків
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.customuser": "fas fa-user",
        "users.profile": "fas fa-id-card",
        "services.service": "fas fa-shopping-bag",
        "services.category": "fas fa-tags",
        "services.serviceimage": "fas fa-images",
        "orders.order": "fas fa-shopping-cart",
        "orders.orderitem": "fas fa-box",
    },

    # Іконки для дій
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Пов'язані модальні вікна
    "related_modal_active": True,

    # Користувацьке меню
    "custom_links": {
    },

    # Переклади для меню
    "language_chooser": True,

    # Переклади для кнопок
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # Переклади для дій
    "show_ui_builder": False,

    # Переклади для пошуку
    "search_model": "users.CustomUser",

    # Переклади для фільтрів
    "topmenu_links": [
        {"name": "Головна", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Веб-сайт", "url": "/", "new_window": True},
    ],

    # Переклади для навігації
    "usermenu_links": [
        {"model": "auth.user"}
    ],

    # Переклади для кнопок дій
    "actions_sticky_top": True,

    # Переклади для заголовків
    "show_sidebar": True,
    "navigation_expanded": True,

    # Переклади для повідомлень
    "custom_css": None,
    "custom_js": None,
}

# Переклади для меню додатків
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}