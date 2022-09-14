# praktikum_new_diplom

![example workflow](https://github.com/cianoid/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание проекта

Продуктовый помощник. Смотрите и создавайте рецепты, подписывайтесь на авторов, добавляйте рецепты в избранное и скачивайте список покупок!

## Варианты запуска проекта

### Запуск проекта в dev-режиме без Docker

#### Клонирование проекта

Сперва клонируйте репозиторий на локальную машину и создайте venv

```
git clone git@github.com:cianoid/foodgram-project-react.git
cd foodgram-project-react
python -m venv venv
source venv/bin/activate
cd backend/foodgram
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Создание .env-файла

С помощью команды ниже в папке будет создан .env-файл 

```
echo 'SECRET_KEY=some-secret-key
ALLOWED_HOSTS=*
DEBUG=1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
' > .env 
```

#### Запуск проекта

Команду loaddata следует запускать только на пустой БД 

```
python manage.py migrate
python manage.py createsuperuser
python manage.py importingredients ingredients.json
python manage.py runserver localhost:8080
```

#### Результат

Будет запущена backend-часть проекта.

API - http://localhost:8080/api/ 

Админка - http://localhost:8080/secure_zone/



### Запуск проекта в контейнерах Docker

#### Клонирование проекта

Сперва клонируйте репозиторий на локальную машину

```
git clone git@github.com:cianoid/foodgram-project-react.git
cd foodgram-project-react/infra
```

#### Создание .env-файла

На production обязательно заменить значение SECRET_KEY

С помощью команды ниже в папке будет создан .env-файл

```
echo 'SECRET_KEY=super-secret
ALLOWED_HOSTS=*
DEBUG=0
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
' > .env
```

#### Сборка контейенеров

Соберите контейнеры и запустите их

```
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

### Заполнение базы данных

Заполните БД подготовленными данными при первом запуске

```
docker compose cp ../data/ingredients.json backend:/app/ingredients.json 
docker compose exec backend python manage.py importingredients ingredients.json
docker compose exec backend rm ingredients.json
```

#### Результат

Будет запущен весь проект.

API - http://localhost/

Redoc - http://localhost/api/docs/

Frontend - http://localhost/

Админка - http://localhost/secure_zone/


### Deploy на сервер
При пуше в ветку master выполняется автоматическое разворачивание проекта на сервере (после всех тестов)


## Об авторе
Шатава Игорь, python-разработчик
