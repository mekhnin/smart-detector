# Smart Animal Detector

![Docker Compose CI](https://github.com/mekhnin/smart-detector/actions/workflows/compose.yaml/badge.svg)

Интеллектуальный сервис обнаружения животных на зашумлённых цифровых изображениях. 

Детекция объектов реализована средствами свёрточной нейронной сети,
шумоподавление — с помощью автоматического анализа сингулярного спектра.

Веб-интерфейс приложения:<br>
![noise reduction example](images/application.png "Веб-интерфейс приложения")

## Список распознаваемых животных
- Птица 🐦
- Кошка 🐈
- Собака 🐶
- Лошадь 🐴
- Овца 🐑
- Корова 🐮
- Слон 🐘
- Медведь 🐻
- Зебра 🦓
- Жираф 🦒

## Технологический стек
- Web UI на Streamlit, Matplotlib
- Асинхронный бэкенд на FastAPI, Celery и RabbitMQ
- Celery для асинхронной обработки задач, RabbitMQ для обмена сообщениями, Redis для кэширования данных
- Микросервис шумоподавления написан на R c использованием Plumber и Rssa
- Инференс нейронных сетей (YOLOv10) на Seldon MLServer

## Пререквизиты
- Для сборки требуется наличие Docker Compose V2.

## Сборка и запуск
- Для старта приложения выполните
```shell
sudo docker compose up -d
```
- Загрузка изображений осуществляется по умолчанию через [веб-интерфейс](http://localhost:8501) на порту 8501. <br>
При необходимости порт можно изменить в переменных окружения:
```shell
echo 'PORT=8080' > .env 
```

## Мониторинг
- Метрики приложения доступны в [**Grafana**](http://localhost:3000).<br>
В качестве **Prometheus** Data source укажите `http://prometheus:9090`.
