# inventory-orders

Простой проект на Django + DRF для управления товарами, корзиной и заказами.
Проект сделан в целях закрепления полученных знаний. Что-то удалось сделать самостоятельно, что-то с помощью ИИ.

Есть над чем работать. Только вперед! 🚀

## 🔧 Технологии
- Python 3.11  
- Django 4.x  
- Django REST Framework  
- JWT Authentication (`djangorestframework-simplejwt`)  
- SQLite (по умолчанию)  
- Swagger / OpenAPI документация  
- pytest / Django TestCase (для тестов)  

---

## 🚀 Установка и запуск

1. Клонировать репозиторий:
```bash
git clone <репозиторий>
cd inventory-orders
```
2. Создать виртуальное окружение и активировать:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Сделать миграции и создать базу данных:
```bash
python manage.py migrate
```

5. Создать суперпользователя (для админки):
```bash
python manage.py createsuperuser
```

6. Запустить сервер:
```bash
python manage.py runserver
```

7. Перейти в браузере:
```bash
API: http://127.0.0.1:8000/api/

Swagger: http://127.0.0.1:8000/swagger/
```
🛠️ Эндпоинты

Products: CRUD (/api/products/)

Cart: add / update / remove / list

Orders / Checkout: /api/checkout/

Auth / JWT: регистрация, login, refresh token