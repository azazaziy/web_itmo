# web_itmo

Сборка контейнера для FastAPI 
```bash
docker build -t fast_api_local ./cmd/db/
```
Запуск консоли FastAPI
```bash
docker-compose -f ./build/docker-compose.yaml run db-api bash
```
Запуск консоли PostgreSQL
```bash
docker-compose -f ./build/docker-compose.yaml run db bash
```
Сборка приложения
```bash
docker-compose -f ./build/docker-compose.yaml up --build
```

Сборка приложения для маков на m1
```bash
docker-compose -f ./build/docker-compose.m1_macs.yaml up --build
```


Запуск приложения
```bash
docker-compose -f ./build/docker-compose.yaml up
```