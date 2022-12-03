# web_itmo

Создание контейнера с для FastAPI 
```bash
docker build -t fast_api_local ./cmd/db/
```
Запуск консоли для FastAPI
```bash
docker-compose -f ./build/docker-compose.yaml run myapp bash
```

Запуск приложения
```bash
docker-compose -f ./build/docker-compose.yaml up
```