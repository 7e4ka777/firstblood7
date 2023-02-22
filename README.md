Задача всего проекта: разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.
Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР (Федерация спортивного туризма России), как только появится доступ в Интернет.
Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.
<br><br>
Контретная цель backender'а: разработка REST API, которое будет обслуживать мобильное приложение.
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
принимает JSON в теле запроса с информацией о перевале. <br> 
Пример JSON:
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
Результатом выполнения метода является JSON-ответ содержащий следующие данные:
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
