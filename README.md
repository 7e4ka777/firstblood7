<h1 align="center">Проект по разработке мобильного приложения для ФСТР</h1>
<h2 align="center">Hi there, I'm <a href="https://github.com/7e4ka777" target="_blank">Ilya</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h2>
<h3 align="center">Computer science student</h3>

**Задача всего проекта**: разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.
Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР (Федерация спортивного туризма России), как только появится доступ в Интернет.
Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.
<br><br>
**Контретная цель backender'а**: разработка REST API, которое будет обслуживать мобильное приложение.

#### Логика работы приложения.
Турист на перевале фотографирует его и вносит следующую информацию с помощью мобильного приложения:
- название объекта и его принадлежность;
- координаты объекта и его высоту;
- сложность объекта, по каждому сезону;
- несколько фотографий;
- информация о пользователе, который передал данные о перевале:
  - данные пользователя (фамилия, имя, отчество);
  - почта;
  - телефон.
При отправке мобильное приложение вызывает метод submitData REST API.
После отправки данных сотрудники ФСТР проводят модерацию для каждого нового объекта и меняют поле status сообщения.

```
Допустимые значения поля status:
	'new' - новая заявка(default-значение);
	'pending' — на рассмотрении;
	'accepted' — заявка принята;
	'rejected' — заявка отклонена.
```

<h1>Описание методов API</h1>
<h2>Метод</h2>

```
POST /submitData/
```

Этот метод принимает JSON в теле запроса с информацией о перевале. <br> 
*Пример JSON*:

```
{
    "beauty_title": "пер.",
    "title": "Пере",
    "other_titles": "Вал",
    "connect": "0",
    "add_time": "2023-02-20 00:13:14",
    "user": {
        "email": "ex@ex.com",
        "fam": "Петров",
        "name": "Петр",
        "otc": "Петрович",
        "phone": "+7 977 777-77-77"
    },
    "coords": {
        "latitude": "32.3476",
        "longitude": "11.3765",
        "height": "2300"
    },
    "level": {
        "winter": "2А",
        "summer": "1А*",
        "autumn": "1А",
        "spring": "2A*"
    },
    "images": [
        {
            "data": "<картинка1>",
            "title": "Основание"
        },
        {
            "data": "<картинка>",
            "title": "Седло"
        },
        {
            "data": "<картинка2>",
            "title": "Обрыв"
        }
    ]
}
```

*Результатом выполнения метода является JSON-ответ содержащий следующие данные*:

```
'status' — код HTTP, целое число:
    200 — запрос успешно обработан;
    400 — Bad Request (при нехватке полей);    
    500 — ошибка при выполнении операции.	
	
'message' — строка:
        Success - отправлено успешно;
	Причина ошибки (если она была);
	
'id' —  идентификатор, который был присвоен объекту 
        при добавлении в базу данных при status=200.
```

*Примеры JSON-ответов*:

```
{ "status": 200, "message": "Success", "id": 42 }
{ "status": 400, "message": "Empty request", "id": null}
{ "status": 500, "message": "Ошибка подключения к базе данных", "id": null}
```

<h2>Метод</h2>

```
GET /submitData/<id>
```

Этот метод получает одну запись (перевал) по её id с выведением всей информацию об перевале, в том числе статус модерации.
*Пример JSON*:

```
{
        "id": 8,
        "user": {
            "id": 7,
            "email": "sem@yandex.ru",
            "fam": "Иванов",
            "name": "Семен",
            "otc": "Олегович",
            "phone": "+7 977 777-77-77"
        },
        "coords": {
            "id": 15,
            "latitude": 7.15,
            "longitude": 5.74,
            "height": 1200
        },
        "levels": {
            "id": 12,
            "winter": "1С",
            "summer": "1А*",
            "autumn": "1А",
            "spring": "1С*"
        },
        "images": [
            {
                "id": 31,
                "created": "2023-02-22T10:46:29.767124",
                "title": "Основание",
                "data": "",
                "pereval": 8
            },
            {
                "id": 22,
                "created": "2023-02-22T10:46:29.769144",
                "title": "Седло",
                "data": "",
                "pereval": 8
            }
        ],
        "created": "2023-02-22T10:41:38.631576",
        "beauty_title": "пер.",
        "title": "Пере",
        "other_titles": "вал",
        "connect": "0",
        "add_time": "2023-02-22T00:00:00",
        "status": "new"
    },
```

*Примеры JSON-ответов*:
```
{ "status": 200, "message": "Success", "id": 42 }
{ "status": 400, "message": "There's no such record", "id": null}
```

<h2>Метод</h2>

```
PATCH /submitData/<id>
```

Позволяет отредактировать существующую запись (замена), если она в статусе "new". 
При этом редактировать можно все поля, кроме ФИО, адреса почты и номера телефона.
<br>В качестве результата изменения приходит ответ содержащий следующие данные: 
- state:
	- 1 — если успешно удалось отредактировать запись в базе данных.
	- 0 — отредактировать запись не удалось.
- message: 
        - сообщение об успешном редактировании при state=1
        - сообщение о причине неудачного обновления записи при state=0.

*Примеры JSON-ответов*:

```
{ "status": 200, "message": "Success", "state": 1 }
{ "status": 400, "message": "It's not a NEW status of the record", "state": 0}
```

<h2>Метод</h2>

```
GET /submitData/?user_email=email
```

Возвращает данные всех объектов, отправленных на сервер пользователем с почтой _email_.<br>
*Пример запроса*: 

```
GET /submitData/?user_email=sem@yandex.ru
```
