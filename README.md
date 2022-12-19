# Проект «Foodgram»
                            
## API

### Требования

- python@3.7.x (возможно работает на версиях выше, но не тестировалось)
- docker
          
### Разработка

1. Склонировать репозиторий и перейти в папку с проектом `foodgram-project-react`.
2. Создать виртуальное окружение `python -m venv venv` и активировать `source ./venv/bin/activate`
3. Установить зависимости локально (для корректной работы редактора и создание миграцией локально) 
```bash
python -m pip install --upgrade pip
pip install -r backend/foodgram/requirements.txt
```
4. Положить в папку `infra` файл `.env`

Шаблон наполнения env-файла:

```shell
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
DJANGO_SECRET_KEY=5555
DJANGO_DEBUG=True
```

5. Запустить docker-compose для разработки (если не указать флаг -d, будут доступны логи, удобно при разработке)
```bash
docker-compose -f docker-compose-dev.yml up --build
```

6. Выполнить миграцию в докер контейнере `django`

```bash
docker-compose exec django python manage.py migrate
```

7. Заполнить базу данных данными

```shell
docker-compose exec django python manage.py loaddata fixtures.json
```

8. Создать суперпользователя для доступа в админку

```bash
docker-compose exec django python manage.py createsuperuser
```

После этого будут доступны:

- Описание эндпоинтов API http://localhost/api/docs/
- Клиентская часть http://localhost/
- Серверная часть API http://localhost:8000/api/
- Админка http://localhost:8000/admin/

### Особенности тестирования API через postman/insomnia/etc

Для запросов, которые требуют авторизации, необходимо предварительно получить токен
                                 
| Метод         |     Адрес     |                                                         Body |
|---------------|:-------------:|-------------------------------------------------------------:|
| POST      | http://localhost:8000/api/auth/token/login | {"email": "<указать email>", "password": "<указать пароль>"} |

Полученный токен использовать в запросах указая в заголовке `Authorization: token <полученный токен>`.

## Автор проекта

По всем вопросам и предложениям можно писать Николаю Ильченко на [почту](tavriaforever@yandex.ru). 
