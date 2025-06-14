## Запуск
1. Скачать проект и открыть его в любом редакторе (Pycharm, VSCode)
2. `python -m venv venv`
3. `pip install -r requirements.txt`
4. `python manage.py runserver`

## Взаимодействие
Для начала нужно нажать кнопку "Зарегистрироваться". Ввести любую почту и пароль. В консоль придёт ссылка на подтвеждение, нужно на нёё нажать. После этого можно авторизоваться под этим пользователем, до подтверждения пользователь не активен.
![image](https://github.com/user-attachments/assets/d373f54a-0ef3-4724-b72d-86cbc22069d3)

## Админ панель

Для управления основными данными есть адмника:
URL - `127.0.0.1:8000/admin`

Данные для входа (под этим пользователем можно также просто авторизоваться на сайте):
```
Email: admin@admin.ru
Password: admin
```


![image](https://github.com/user-attachments/assets/b001bb70-3651-4ecc-9fce-dbf5dc84587b)


## Карта основных страниц сайта:
- `127.0.0.1:8000/profile/` - ЛК пользователя
- `127.0.0.1:8000/profile/edit/` - редактирование профиля
- `127.0.0.1:8000/authors/` - авторы
- `127.0.0.1:8000/author_profile/<id>` - профиль автора
- `127.0.0.1:8000/stories/` - список рассказов
- `127.0.0.1:8000/audiobooks/` - просмотр аудиокниг
- `127.0.0.1:8000/blogs/` - блог
- `127.0.0.1:8000/auth/` - авторизация
- `127.0.0.1:8000/register/` - регистрация
- `forgot_password/` - форма восстановления пароля
- `127.0.0.1:8000/chart/` - графики

## Превью основных страниц

### Главная страница
![image](https://github.com/user-attachments/assets/efb3db26-8faf-4dcf-bf66-416c8424aca0)

### Профиль
![image](https://github.com/user-attachments/assets/ec4831b9-0925-4b7a-95ea-cccaa276fb2c)

### Просмотр страницы автора
![image](https://github.com/user-attachments/assets/603f6748-8e0a-44e3-b842-c89b1652e529)

### Список стихов
![image](https://github.com/user-attachments/assets/7e9fa3a6-0d7d-4207-afe7-bb1a700b7b99)

### Аудиокнига
![image](https://github.com/user-attachments/assets/26b36c0c-27b9-428f-9928-43f68dcca1b3)

### Графики
![image](https://github.com/user-attachments/assets/aa9d6c17-9e2c-4159-b14b-99aee82ab543)

