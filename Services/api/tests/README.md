# Notes

To run tests local (Docker) selenium, redis and celery should be created with the following configuration (in docker compose):
```
selenium:
    image: selenium/standalone-chrome
    container_name: selenium
    restart: unless-stopped
    ports:
        - 4444:4444
```

```
redis:
    image: redis:7
    container_name: redis_app
    restart: unless-stopped
    ports:
      - 6379:6379
    healthcheck:
      test: [ "CMD", "redis-cli","ping" ]
      interval: 5s
      retries: 5
    networks:
      - backend
```
```
celery:
    build:
      context: api/
    container_name: celery_app
    command: [ "/fastapi_app/scripts/celery.sh", "celery" ]
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - backend
```
