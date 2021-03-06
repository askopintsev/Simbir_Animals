# Руководство по запуску приложения

Чтобы запустить приложение необходимо выполнить следующие 
условия:

1. Установить интерпретатор Python 3.

   - если интерпретатор отсутствует, пройдите по ссылке 
   [Python.org](https://www.python.org/downloads/) 
   и следуйте инструкциям установщика
   
1. Окружение Python должно соответствовать требованиям запуска приложения.
Требования указаны в файле **requirements.txt** в каталоге приложения.
   - для установки необходимых библиотек можно 
   воспользоваться менеджером пакетов, с помощью команды:
    `pip install -r requirements.txt`
   
1. *Опционально, если используются виртуальные окружения.
Запустить окружение Python, удовлетворяющее требованиям запуска.
 Экземпляр доступен в директории приложения в папке **venv**.
   
1. Запустить сервер Flask через командную строку, находясь
в директории приложения Simbir_Animals, с помощью команды:
 `flask run`
 
1. Перейти по ссылке [http://localhost:5000/](http://localhost:5000/), 
чтобы открыть стартовую страницу
    
   

# Руководство пользователя
Веб-сервис Simbir Animals предоставлет возможность получить 
случайное изображение животного для созерцания с возможностью
последующего повторного просмотра изображения из истории
запросов.

В данной версии сервис предоставляет следующий функционал:

- запрос случайного изображения животного
- просмотр полной истории запросов изображений
- просмотр конкретного изображения из истории запросов

## Главная страница сервиса

Главная страница сервиса предоставляет меню навигации по доступным разделам:

- Cat page
- Dog page
- Fox page
- History
- Image by Uuid

Чтобы попасть на главную страницу из любого раздела сервиса, 
необходимо воспользоваться стандартным функционалом браузера 
"Вернуться на предыдущую страницу".

## Запрос случайного изображения животного

Чтобы запросить случайное изображение животного необходимо
перейти по соответствующей ссылке меню навигации или 
набрать интересующий адрес в строке поиска вашего браузера.

В данной версии возможен запрос изображений следующий животных:
- Кошка
- Собака
- Лиса

### Запрос изображения кошки

Чтобы запросить случайное изборажение кошки, необходимо:

- на главной странице перейти по ссылке пункта меню **"Cat page"**
- или добавить к имени сервиса в адресной строке браузера
адрес: **/animal/cat**

В результате данного запроса вы получите случайное изображение
кошки, обработанное оригинальным фильтром.

Все запросы сохраняются в Истории запросов и в дальнейшем 
доступны для просмотра.

### Запрос изображения собаки

Чтобы запросить случайное изборажение собаки, необходимо:

- на главной странице перейти по ссылке пункта меню **"Dog page"**
- или добавить к имени сервиса в адресной строке браузера
адрес: **/animal/dog**

В результате данного запроса вы получите случайное изображение
собаки, обработанное оригинальным фильтром.

Все запросы сохраняются в Истории запросов и в дальнейшем 
доступны для просмотра.

### Запрос изображения лисы

Чтобы запросить случайное изборажение лисы, необходимо:

- на главной странице перейти по ссылке пункта меню **"Fox page"**
- или добавить к имени сервиса в адресной строке браузера
адрес: **/animal/fox**

В результате данного запроса вы получите случайное изображение
лисы, обработанное оригинальным фильтром.

Все запросы сохраняются в Истории запросов и в дальнейшем 
доступны для просмотра.

### История запросов

Чтобы просмотреть историю запросов изображений, необходимо:

- на главной странице перейти по ссылке пункта меню **"History"**
- или добавить к имени сервиса в адресной строке браузера
адрес: **/history**

История запросов предоставляет возможность просмотра
следующей информации о запросе:

- идентификатор запроса
- вид животного, изображение которого было запрошено
- имя файла изображения животного
- время запроса (по часовому поясу GMT)

### Просмотр конкретного изображения из истории

Сервис предоставляет возможность повторного просмотра
 изображений.
 
 Чтобы просмотреть конкретное изображение из истории 
 запросов, необходимо добавить к имени сервиса в адресной строке браузера
адрес: **/history/static/uuid**,

где uuid - имя избражения в формате UUID версии 4.

Также при переходе по ссылке пункта меню **"Image by Uuid"** 
возможно перейти в раздел, где можно указывать только uuid
файла в дополнение к указанному адресу в адресной строке.

При запросе просмотра изображения необходимо указывать только
его uuid, то есть имя без указания расширения файла.
