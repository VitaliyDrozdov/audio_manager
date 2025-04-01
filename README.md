# audio_manager v 0.1.0
Audio manager using FastAPI


<h1 align="center"> MVP аудиозагрузчика </h1>


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

## 🚀 Запуск локальный

</h2>



<p>


- В папке с проектом переименовать файл ".env.example" в ".env". В нем содержатся переменные настроек.


- Запустить Docker и выполнить команду:


```text
docker compose up --build
```

После успешного запуска контейнеров, выполните следующую команду, выполнит миграции:

```shell
docker exec -it audio_manager_project-backend-1 sh -c "alembic upgrade head"
```
</p>

Документация будет доступна по адресу:

```text
http://localhost:8100/docs
```


При старте будет создан суперпользователь. Данные суперпользователя настраиваются в .env. По-умолчанию данные такие:

```
SUPERUSER_EMAIL=super@example.com
SUPERUSER_USERNAME=superuser
SUPERUSER_PASSWORD=superpassword
```

Чтобы авторизироваться через Яндекс нужно пройти по ссылке-редирект. После чего в консоли выведется сгененированная ссылка от Яндекс API. Например:
```
https://oauth.yandex.ru/authorize?response_type=code&client_id=2d8e37fed02640e887046dc488152f5b&force_confirm=yes
```
Далее нужно перейти по этой ссылке и залогиниться в свой аккаунт.


## Автор :

[VitaliyDrozdov](https://github.com/VitaliyDrozdov)
