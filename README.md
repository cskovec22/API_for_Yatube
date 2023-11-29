# Проект «API для Yatube»
Данное API предназначено для просмотра и создания публикаций.  
Публикации могут находиться в группах.  
Просматривать публикации может любой пользователь, а создавать их и комментировать - только авторизованный пользователь.  
Редактировать и изменять можно только свои объекты.  
Также авторизованный пользователь может подписаться на других авторов, кроме себя. Просматривать подписки других пользователей нельзя.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:  
```
https://github.com/cskovec22/api_final_yatube
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
py -m venv venv
```
```
. venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
py -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
py manage.py migrate
```
Запустить проект:
```
py manage.py runserver
```

### Примеры запросов к API:  
#### Получение публикаций  
```
GET /api/v1/posts/
```
При указании параметров _limit_ (количество публикаций на страницу) и _offset_ (номер страницы, после которой начинать выдачу) выдача работает с пагинацией.  
```
GET /api/v1/posts/?limit=4&offset=2
```
Пример удачного выполнения запроса:
```
{
  "count": 13,
  "next": "http://api.example.org/accounts/?offset=9&limit=4",
  "previous": .../?offset=5&limit=4",
  "results": [
    {}
  ]
}
```
#### Создание публикации  
Анонимные запросы запрещены.
```
POST /api/v1/posts/
```
Тело запроса:
```
{
  "text": "string", - обязательное поле, string (текст публикации)
  "image": "string", - string or null <binary>
  "group": 0 - integer or null (id сообщества)
}
```
Пример удачного выполнения запроса:
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2023-11-30T14:15:22Z",
  "image": "string",
  "group": 0
}
```
#### Получение публикации  
Получение публикации по id.
```
GET /api/v1/posts/{id}/
```
#### Обновление публикации  
Обновление публикации по id. Обновить публикацию может только автор публикации. Анонимные запросы запрещены.
```
PUT /api/v1/posts/{id}/
```
Тело запроса:
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
#### Частичное обновление публикации
Частичное обновление публикации по id. Обновить публикацию может только автор публикации. Анонимные запросы запрещены.
```
PATCH /api/v1/posts/{id}/
```
Тело запроса:
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
#### Удаление публикации
Удаление публикации по id. Удалить публикацию может только автор публикации. Анонимные запросы запрещены.
```
DELETE /api/v1/posts/{id}/
```
#### Получение комментариев
Получение всех комментариев к публикации.
```
GET /api/v1/posts/{post_id}/comments/
```
Пример удачного выполнения запроса:
```
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2023-11-30T14:15:22Z",
    "post": 0
  }
]
```
#### Добавление комментария
Добавление нового комментария к публикации. Анонимные запросы запрещены.
```
POST /api/v1/posts/{post_id}/comments/
```
Тело запроса:
```
{
  "text": "string" - обязательное поле, string (текст комментария)
}
```
Пример удачного выполнения запроса:
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2023-11-30T14:15:22Z",
  "post": 0
}
```
#### Получение комментария
Получение комментария к публикации по id.
```
GET /api/v1/posts/{post_id}/comments/{id}/
```
Пример удачного выполнения запроса:
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2023-11-30T14:15:22Z",
  "post": 0
}
```
#### Обновление комментария
Обновление комментария к публикации по id. Обновить комментарий может только автор комментария. Анонимные запросы запрещены.
```
PUT /api/v1/posts/{post_id}/comments/{id}/
```
Тело запроса:
```
{
  "text": "string"
}
```
#### Частичное обновление комментария
Частичное обновление комментария к публикации по id. Обновить комментарий может только автор комментария. Анонимные запросы запрещены.
```
PATCH /api/v1/posts/{post_id}/comments/{id}/
```
Тело запроса:
```
{
  "text": "string"
}
```
#### Удаление комментария
Удаление комментария к публикации по id. Обновить комментарий может только автор комментария. Анонимные запросы запрещены.
```
DELETE /api/v1/posts/{post_id}/comments/{id}/
```
#### Список сообществ
Получение списка доступных сообществ.
```
GET /api/v1/groups/
```
Пример удачного выполнения запроса:
```
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
```
#### Информация о сообществе
Получение информации о сообществе по id.
```
GET /api/v1/groups/{id}/
```
#### Подписки
Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены.
```
GET /api/v1/follow/
```
Пример удачного выполнения запроса:
```
[
  {
    "user": "string",
    "following": "string"
  }
]
```
Возможен поиск по подпискам по параметру _search_.
#### Подписка
Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса. Анонимные запросы запрещены.
```
POST /api/v1/follow/
```
Тело запроса:
```
{
  "following": "string"
}
```
#### Получить JWT-токен
Получение JWT-токена.
```
POST /api/v1/jwt/create/
```
Тело запроса:
```
{
  "username": "string",
  "password": "string"
}
```
Пример удачного выполнения запроса:
```
{
  "refresh": "string",
  "access": "string"
}
```
Токен вернётся в поле _access_, а данные из поля _refresh_ пригодятся для обновления токена.
#### Обновить JWT-токен
Обновление JWT-токена.
```
POST /api/v1/jwt/refresh/
```
Тело запроса:
```
{
  "refresh": "string"
}
```
Пример удачного выполнения запроса:
```
{
  "access": "string"
}
```
#### Проверить JWT-токен
Проверка JWT-токена.
```
POST /api/v1/jwt/verify/
```
Тело запроса:
```
{
  "token": "string"
}
```
