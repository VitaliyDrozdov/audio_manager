# audio_manager v 0.1.0
Audio manager using FastAPI


<h1 align="center"> MVP аудиозагрузчика. </h1>


<hr>

</p>
<h2 align="center">

### Используемый стек:<a name="stack"></a>

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Docker
- Poetry
- Pre-commit

## 📍 Описание

<p>
Пользователи регистрируются либо обычным методом через почту и пароль, либо через Yandex OAuth 2.0. Перед запуском приложения создается суперпользователь с максимальными правами.
Пользователи могут загружать и просматривать свои аудиофайлы.
Хранилище реализовано на локальном диске. Расширения файлов проверяются Pydantic на тип "аудио".

</p>



<h2 align="center">

## 🚀 Запуск локальныйы

</h2>



<p>


- В папке с проектом переименовать файл ".env.example" в ".env". В нем содержатся переменные настроек.


- Запустить Docker и выполнить команду:


```text
docker compose up --build -d
```

</p>

Документация будет доступна по адресу:

```text
http://localhost:8100/docs
```


При старте будет созда суперпользователь. Данные суперпользователя настраиваются в .env. По-умолчанию данные такие:

```
SUPERUSER_EMAIL=super@example.com
SUPERUSER_USERNAME=superuser
SUPERUSER_PASSWORD=superpassword
```

## Автор :

[VitaliyDrozdov](https://github.com/VitaliyDrozdov)
