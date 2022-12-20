# Проект «Foodgram»

Проект сделан в декабре 2022 года, в рамках дипломной работы на курсе Яндекс.Практикум "Python-разработчик". 

- Основной проект https://myfoodgram.ddns.net/
- API https://myfoodgram.ddns.net/api/

## Админка 
           
- Адрес: https://myfoodgram.ddns.net/admin/
- Email: admin@admin.ru
- Второе поле: test_password_2022

## Директории

- `backend` - API для фронтенда на django 2.2 + django-rest-framework 3.12 + postgresql 13
- `docs` - Документация к API, доступна по адресу https://myfoodgram.ddns.net/api/docs/ 
- `frontend` - исходники клиентской части на `React.js`, работает без сервера, статика собирается во время запуска `docker-compose` и раздаётся c помощью `nginx`.
- `infra` - содержит конфигурации для запуска проекта целиком `docker-compose` и `nginx`. 
                            
## API

### Требования

- Python@3.7.x (возможно работает на версиях выше, но не тестировалось)
- Docker
          
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

После этого локально на компьютере будут доступны:

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

### Линтеры

Установите пре-коммит хуки
```bash
   pre-commit install
```

После этого на `git` коммиты будет запускаться модуль `black` для автоформатирования кода и `flake8` для проверки кода на соответствие `PEP8`.
             

## CI

Для удобства разработки и деплоя, настроен CI через github actions. Конфигурация расположена в директории [.github/workflows/foodgram_workflow.yml](./.github/workflows/foodgram_workflow.yml).

При каждом `push` в ветку `master`:
- линтинг файлов с помощью Flake8;
- сборка и загрузка докер образа c файлами API в репозиторий [tavriaforever/foodgram-backend](https://hub.docker.com/repository/docker/tavriaforever/foodgram-backend);
- деплой проекта на боевой сервер в Яндекс.Облако.

## HTTPS сертификаты

Для боевого сервера сгенерированы сертификаты через [certbot](https://github.com/certbot/certbot).

Если понадобиться пересоздать:
                     
1. Создать сертификат для установки в nginx
```bash
sudo certbot certonly -d myfoodgram.ddns.net
```

2. Убедиться, что указан сертификат с текущим доменом в [infra/nginx/default.conf](./infra/nginx/default.conf) конфиге для боевого сервера.
```bash
ssl_certificate /etc/letsencrypt/live/myfoodgram.ddns.net/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/myfoodgram.ddns.net/privkey.pem;
```

## Автор проекта

По всем вопросам и предложениям можно писать Николаю Ильченко на [почту](tavriaforever@yandex.ru). 
