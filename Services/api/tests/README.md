# Notes

To run tests local (Docker) selenium and db should be created with the following configuration (in docker compose)
```
selenium:
    image: selenium/standalone-chrome
    container_name: selenium
    restart: unless-stopped
    ports:
        - 4444:4444
```
```
# Same to the main api/.env file
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
