# Скачиваем изображение космоса и отправляем их в телеграм

![imageup.ru](https://api.nasa.gov/EPIC/archive/natural/2019/05/30/png/epic_1b_20190530011359.png?api_key=DEMO_KEY)
## О проекте: 

Содержит четыре скрипта
1. `epic_image_download.py` качает изображение через API - https://api.nasa.gov/ 
[![imageup.ru](https://imageup.ru/img66/3990243/chrome_vk1pf4jils.png)](https://imageup.ru/img66/3990243/chrome_vk1pf4jils.png.html)
    * качает фотографии с архива Nasa, которые были сделаны телескопом "EPIC";
    * создаёт в директории проекта паку `image`.

2. `nasa_image_download.py`  качает изображение через API - https://api.nasa.gov/
[![imageup.ru](https://imageup.ru/img169/3990246/chrome_bctr4faxhc.png)](https://imageup.ru/img169/3990246/chrome_bctr4faxhc.png.html)
   * качает случайные фотографии с архива Nasa;
   * создаёт в директории проекта паку `image`.
    
3. `spacex_image_download.py` использует API лежащую в открытом доступе на github - https://github.com/r-spacex/SpaceX-API
    * имеет две вариации работы:
      * качает фотографии последнего запуска;
      * качает фотографии по ID полёта.
    * создаёт в директории проекта паку `image`.

4. `send_file_in_telegram.py` отправляет файл в телеграм канал.
    * может отправить все файлы из папки;
    * может отправить один файл из директории, где лежит проект.

## Как подготовить проект к запуску

1. Создайте файл  `.env`  в директории проекта.
2. В файл  `.env`  добавьте строки со значениями:
   - `TELEGRAM_BOT_KEY="Ваш API ключ"`
   - `TELEGRAM_CHAT_ID="@ID вашего канала"`
   - `NASA_API_KEY="Ваш API ключ"`

#### Как получить API ключи и создать канал в телеграм:

`TELEGRAM_BOT_KEY` можно получить при создании бота в телеграм, как это сделать - https://botcreators.ru/blog/botfather-instrukciya/
[![imageup.ru](https://imageup.ru/img120/3990253/telegram_trpah8babz.jpg)](https://imageup.ru/img120/3990253/telegram_trpah8babz.jpg.html)

`TELEGRAM_CHAT_ID` как создать канал - https://www.easydoit.ru/telegram/kak-dobavit-bota-v-kanal-telegram/

`NASA_API_KEY` что бы получить API nasa надо перейти на сайт - https://api.nasa.gov/ и заполнить форму "Generate API Key"
[![imageup.ru](https://imageup.ru/img154/3993663/chrome_327t9ltrsk.png)](https://imageup.ru/img154/3993663/chrome_327t9ltrsk.png.html)


__Важное!__ Телеграм бот должен быть админом в вашем канале.

## Подробнее о скриптах и как их запустить

### Запуск `epic_image_download.py`

Скрипт `epic_image_download.py` качает изображение в папку `"image"`.

Загружает изображение в папку `image`, которая будет находиться в директории проекта.

Пример запуска:

```python
python epic_image_download.py
```


### Запуск `nasa_image_download.py` 

Загружает изображение в папку `image`, которая будет находиться в директории проекта.
Можно указать количество загружаемых фотографии.

* `--number_of_photos_to_upload` - указывает какое количество картинок надо скачать. По дефолту скачивает 15 картинок.

Пример запуска:

```python
python nasa_image_download.py --number_of_photos_to_upload 20
```

### Запуск `spacex_image_download.py` 
Скрипт ожидает один аргумент:

* `--launch_id` - id запуска, если он не указан скачает фото с последнего запуска, если на последнем запуске не было фотографии сообщит об этом.

* Для тестов можете использовать следующий id запуска- `"5eb87d47ffd86e000604b38a"`.
  
Скачивает фотографии с последнего запуска или по заданному ID в папку `image`, которая будет находиться в директории проекта.

Пример запуска:

1. Скачать фото по ID запуска
```python
  python spacex_image_download.py --launch_id "5eb87d47ffd86e000604b38a"
```
2. Скачать фотографии последнего запуска
```python
  python spacex_image_download.py
```

### Запуск `send_file_in_telegram.py`

Перед запуском скрипта:
1. Убедитесь что телеграм бот создан и добавлен в группу.
2. Токен который получили при создании бота и ID канала указаны в `.env`
Скрипт отправляет один файл или все файлы из папки в телеграм канал.

Аргументы для запуска скрипта:
* `--folder_name` - указываем название папки из которой будут отправлены файлы.
* `--file_name` - имя файла, которого необходимо отправить. ука
* `--delay_before_send` - время, указывается в секундах, отправки изображений в Телеграм чат, по дефолту, отправка будет осуществлять раз в 14400 сек(4 часа)


Скрипт работает по двум сценариям:
1. Отправка одного изображения, из директорий в которой лежит скрипт

   * Для отправки файла, необходимо полностью указать его имя и расширение, пример - `Nasa_apod0.jpg`

Пример запуска:
```python
python send_file_in_telegram.py --image_name "Nasa_apod_0.jpg"
```

2. Отправка всех изображений из указанной папки, папка должна находиться в директории проекта. Отправка происходит с заданной задержкой.

Пример запуска:
```python
python send_file_in_telegram.py --folder_name "image" --delay_before_send 10
```


## Требования к окружению

Python3 должен быть уже установлен.
Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```python
pip install -r requirements.txt
```



