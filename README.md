# API_final

<<<<<<< HEAD
## Работа с постами с разделением прав (авторизованный и неавторизованный пользователь).

=======
>>>>>>> 7a02a4e548dbc18394bb6c6dcd1b5a76e80a3c15
### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:  

```
git clone https://github.com/SheRodion/api_final_yatube.git
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:
```
cd yatube_api
```
```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
``
