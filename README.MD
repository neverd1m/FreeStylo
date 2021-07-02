### Краткое описение
Тестовое задание в компанию Free.Stylo

##### Копирование репозитория
`mkdir freestylo`  
`cd freestylo/`  
`git clone git@github.com:neverd1m/FreeStylo.git`  

##### Создание отдельного виртуального контейнера для проекта. 
`virtualenv freestylo_env`    
##### Запуск окружения, в дальнейшем всегда обязательная компанда для запуска сервиса
`source freestylo_env/bin/activate`      
##### Установка необходимых библиотек для проекта внутри запущенного окружения
`cd FreeStylo/`  
`pip3 install -r requirements.txt`  

## Обновление базы данных
`./manage.py makemigrations`  
`./manage.py migrate`

##### Создание образа docker
`docker build --tag freestylo_image .`  

##### Запуск образа docker
`docker run --net host -p 8000:8000 freestyle_image`


### Комментарии
На моей локальной машине я устанавливал [memcached](https://hub.docker.com/_/memcached) глобально, поэтому образ Docker для него не использовал. При необходимости **memcached** можно использовать через docker-compose вместе с образом проекта, и тогда параметр *--network host* не нужен.

### Пункты, до которых добраться не успел:
1. Асинхронное выполнение;
2. Валидация данных;
3. Написание тестов.

