# Notes

To run tests local (Docker) selenium should be created with the following configuration (in docker compose)
```
selenium:
    image: selenium/standalone-chrome
    container_name: selenium
    restart: unless-stopped
    ports:
        - 4444:4444
```
