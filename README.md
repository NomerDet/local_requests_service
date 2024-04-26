# Веб-сервис для локальной обработки заявок
Проект позволяет осуществлять обработку заявок в отсутствии сети интернет и синхронизацию МастерБД (сайт) -> ЛокалБД.

Для сборки выполнить команду:

`sudo docker buildx create --use --driver=docker-container && sudo docker buildx build --platform linux/arm64 --cache-to type=local,dest=/home/ubuntu/cache --cache-from type=local,src=/home/ubuntu/cache . -t docker1mainsaonline/aicameras:hub_main_backend_arm  -f ./docker/Dockerfile --push`

Для отладки необходимо предварительно собрать: https://github.com/NomerDet/celery_service

Далее можно использовать такой docker-compose.yml:

```
version: '2'
services:

  backend:
    restart: always
#    image: docker1mainsaonline/aicameras:hub_main_backend_j_test
    image: docker1mainsaonline/aicameras:hub_main_backend_amd_test
    ports:
      - "443:443"
    command: ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/root/.local/share/mkcert/backend+4-key.pem", "--ssl-certfile", "/root/.local/share/mkcert/backend+4.pem"]
    volumes:
      - ./configs:/app/configs
      - ./local_requests_service:/app
    depends_on:
      - worker
      - beat
#      database:
#        condition: service_healthy

  beat:
#    image: docker1mainsaonline/aicameras:hub_main_celery_j_test
    image: docker1mainsaonline/aicameras:hub_main_celery_amd_test
    restart: unless-stopped
    environment:
      - CONFIG=/app/configs/config.yaml
      - CLONE_TIME_PERIOD=20
      - UPDATE_TIME_PERIOD=10
    command: celery -A tasks beat --loglevel=debug
    volumes:
      - ./configs:/app/configs
      - ./celery:/app
    depends_on:
      - worker

  worker:
#    image: docker1mainsaonline/aicameras:hub_main_celery_j_test
    image: docker1mainsaonline/aicameras:hub_main_celery_amd_test
    restart: unless-stopped
    environment:
      - CONFIG=/app/configs/config.yaml
      - CLONE_TIME_PERIOD=20
      - UPDATE_TIME_PERIOD=10
    command: celery -A tasks worker --loglevel=debug -E
    volumes:
      - ./configs:/app/configs
      - ./celery:/app
    depends_on:
      redis:
        condition: service_started
      database:
        condition: service_healthy

  redis:
#    image: arm64v8/redis:7-alpine
    image: redis:7-alpine
    restart: unless-stopped
    expose:
      - 6379

  database:
#    image: docker1mainsaonline/aicameras:hub_main_mysql_j_test
    image: docker1mainsaonline/aicameras:hub_main_mysql_amd_test
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=JLK32PO!32cfx
      - TZ=Europe/Moscow
    #https://dev.to/gustavorglima/disabling-onlyfullgroupby-on-mysql-docker-laravel-sail-bob
    command:
      --sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
    healthcheck:
      test: mysqladmin ping -h 127.0.0.1 -u root --password=$$MYSQL_ROOT_PASSWORD
      timeout: 10s
      retries: 3
    expose:
      - 3306
    ports:
      - 3306:3306
    volumes:
      - mysql_data:/var/lib/mysql
      - ./configs:/app/configs
      - ./docker/localdb/mysql/init/mysql_entrypoint.sh:/docker-entrypoint-initdb.d/mysql_entrypoint.sh

volumes:
  mysql_data:
```

Для отладки оффлайн работы можно использовать IPTABLES (https://habr.com/ru/articles/473222/):
- `sudo iptables -L -n -v` - узнать название сети
- `sudo iptables -I DOCKER-USER -i ens3 -o br-9f0ef0b16930 -j DROP` - _Первом делом ведем правило DROP для всех подключений в сеть_
- `sudo iptables -I DOCKER-USER -i ens3 -s 95.165.0.13 -j RETURN` - _Разрешим соединение для одного ip адреса, точнее сказать пакет может продолжить путь дальше по FORWARD._

[TODO] Проект требует обязательного создания тестов.

Ниже описан оригинальный проект, который использовался как шаблон.

# fastapi-clean-example

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://black.readthedocs.io/en/stable/)
[![Typed with: pydantic](https://img.shields.io/badge/typed%20with-pydantic-BA600F.svg?style=for-the-badge)](https://docs.pydantic.dev/)
[![Open Issues](https://img.shields.io/github/issues-raw/0xTheProDev/fastapi-clean-example?style=for-the-badge)](https://github.com/0xTheProDev/fastapi-clean-example/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/0xTheProDev/fastapi-clean-example?style=for-the-badge)](https://github.com/0xTheProDev/fastapi-clean-example/issues?q=is%3Aissue+is%3Aclosed)
[![Open Pulls](https://img.shields.io/github/issues-pr-raw/0xTheProDev/fastapi-clean-example?style=for-the-badge)](https://github.com/0xTheProDev/fastapi-clean-example/pulls)
[![Closed Pulls](https://img.shields.io/github/issues-pr-closed-raw/0xTheProDev/fastapi-clean-example?style=for-the-badge)](https://github.com/0xTheProDev/fastapi-clean-example/pulls?q=is%3Apr+is%3Aclosed)
[![Contributors](https://img.shields.io/github/contributors/0xTheProDev/fastapi-clean-example?style=for-the-badge)](https://github.com/0xTheProDev/fastapi-clean-example/graphs/contributors)
[![Activity](https://img.shields.io/github/last-commit/0xTheProDev/fastapi-clean-example?style=for-the-badge&label=most%20recent%20activity)](https://github.com/0xTheProDev/fastapi-clean-example/pulse)

## Description

_Example Application Interface using FastAPI framework in Python 3_

This example showcases Repository Pattern in Hexagonal Architecture _(also known as Clean Architecture)_. Here we have two Entities - Books and Authors, whose relationships have been exploited to create CRUD endpoint in REST under OpenAPI standard.

## Installation

- Install all the project dependency using [Pipenv](https://pipenv.pypa.io):

  ```sh
  $ pipenv install --dev
  ```

- Run the application from command prompt:

  ```sh
  $ pipenv run uvicorn main:app --reload
  ```

- You can also open a shell inside virtual environment:

  ```sh
  $ pipenv shell
  ```

- Open `localhost:8000/docs` for API Documentation

- Open `localhost:8000/graphql` for GraphQL Documentation

_*Note:* In case you are not able to access `pipenv` from you `PATH` locations, replace all instances of `pipenv` with `python3 -m pipenv`._

## Testing

For Testing, `unittest` module is used for Test Suite and Assertion, whereas `pytest` is being used for Test Runner and Coverage Reporter.

- Run the following command to initiate test:
  ```sh
  $ pipenv run pytest
  ```
- To include Coverage Reporting as well:
  ```sh
  $ pipenv run pytest --cov-report xml --cov .
  ```

## License

&copy; MIT License
