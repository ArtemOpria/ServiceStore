#!/usr/bin/env python
"""
Скрипт для компіляції файлів перекладів (.po в .mo)
Запустіть цей скрипт після редагування файлів перекладів
"""

import os
import subprocess
from pathlib import Path

# Отримуємо шлях до кореневої директорії проекту
BASE_DIR = Path(__file__).resolve().parent

# Шлях до директорії з перекладами
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')

def compile_messages():
    """
    Компілює всі файли перекладів (.po) в бінарні файли (.mo)
    """
    print("Компіляція файлів перекладів...")
    
    # Перевіряємо, чи існує директорія locale
    if not os.path.exists(LOCALE_DIR):
        print(f"Директорія {LOCALE_DIR} не існує. Створюємо...")
        os.makedirs(LOCALE_DIR)
    
    try:
        # Запускаємо команду компіляції
        result = subprocess.run(
            ['django-admin', 'compilemessages'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        print("Успішно скомпільовано файли перекладів!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Помилка при компіляції файлів перекладів: {e}")
        print(f"Вивід помилки: {e.stderr}")
    except Exception as e:
        print(f"Виникла непередбачена помилка: {e}")

if __name__ == "__main__":
    compile_messages()
    print("\nДля активації перекладів переконайтеся, що в settings.py встановлено:")
    print("LANGUAGE_CODE = 'uk'")
    print("USE_I18N = True")
    print("USE_L10N = True")
    print("\nТакож переконайтеся, що middleware 'django.middleware.locale.LocaleMiddleware' додано до MIDDLEWARE")