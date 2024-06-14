# Building a news graph and services around it

[![Services Build Status](https://github.com/FlameInBrainSerj/project_news_graph/actions/workflows/services.yml/badge.svg?branch=main)](https://github.com/FlameInBrainSerj/project_news_graph/actions/workflows/services.yml) [![Pipeline Build Status](https://github.com/FlameInBrainSerj/project_news_graph/actions/workflows/pipeline.yml/badge.svg?branch=main)](https://github.com/FlameInBrainSerj/project_news_graph/blob/main/.github/workflows/pipeline.yml)

**Curator:** Andrey Babynin (@maninoffice)

**Team members:** Maxim Dumenkov (@maxodum), Sergey Krivosheev (@FlameInBrain)

**Project description:** Construction of NLP models to analyze the impact of news on financial instruments and construction of graph for analysis of financial entities interconnections

**Project structure:**
- Research: repository with the .ipynb files containing the processes of data collection, EDA and modeling experiments
- Pipeline: repository containing automated process of new data collection, data preprocessing, model training and inferencing
- Services: repository containing API for interacting with final models for getting predictions, Telegram Bot as users UI and Streamlit as interactive dashboard of EDA of collected data

**Project functionality:**
- [API](http://185.209.31.172:8189/docs)
    - /model/predict_by_link - get prediction of impact of news on financial instruments by news' link
    - /model/predict_by_links_batch - get prediction of impact of news on financial instruments by batch of news' links (.csv file with first row skipped and all the links placed row by row in first column must be passed)
    - /model/predict_by_text - get prediction of impact of news on financial instruments by news' text
    - /model/predict_by_texts_batch - get prediction of impact of news on financial instruments by batch of news' texts (.csv file with first row skipped and all the texts placed row by row in first column must be passed)
- [Telegram Bot](https://t.me/project_news_anal_bot)
    - Get information about the service and the project
    - Disclaimer (some minor details that must be kept in mind)
    - Get prediction by link or text of the news
    - Rate the app
    - Get statistics of the app' rating and the users' comments
    - Get information about the ticker from MOEX top-100
    - Get the graph of financial entities
- Streamlit (TBA)
    * Interactive dashboard of EDA of collected data


**Docker-compose content description:**
- Portainer: Container manager
- Bot: Telegram Bot
    - Dockerfile: setting up the environment and starting the app
- API: FastAPI
    - Dockerfile: setting up the environment and giving executable status to scripts required for the API start using gunicorn and start of the celery and the flower
- Nginx: Proxy for API
- Redis: Caching and brokerage for celery
- Postgres: Database for users' ratings and reviews
- Celery & Flower: Asynchronous queue of tasks and the UI for this
- Selenium: Parsing of the texts of the news on the news websites
- Prometheus & Grafana: Services monitoring and better UI for this

**Project assembling instruction:**

1. Clone the repo on your machine
```
git clone https://github.com/FlameInBrainSerj/project_news_graph.git
```
2. In folders Services/api and Services/bot create .env files from .env.example with the following configuration
```
# bot/.env

# Needs to be created using BotFather
BOT_TOKEN=your_bot_token

DB_HOST=db
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API_HOST=api
API_PORT=8000
```
```
# api/.env

REDIS_HOST=redis
REDIS_PORT=6379

SELENIUM_HOST=selenium
```
3. Get all the artifacts (models and tokenizers folders) from the [storage](https://disk.yandex.ru/d/sdQmEjHlah6BBg) and place them in Services/api/artifacts folder
4. Start the docker containers
```
docker compose up
```
5. Remove the docker containers
```
docker compose down
```
