# Building a news graph and services around it

[![Service-bot Build Status](https://github.com/FlameInBrainSerj/project_news_graph/actions/workflows/service_bot.yml/badge.svg?branch=main)](https://github.com/FlameInBrainSerj/project_news_graph/actions/workflows/service_bot.yml)

**Curator:** Andrey Babynin (@maninoffice)

**Team members:** Maxim Dumenkov (@maxodum), Sergey Krivosheev (@FlameInBrain)

**Project description:** Parsing news, analyzing them using NLP and GNN methods and creating services around the resulting models, namely:
* Creation of NLP models that evaluate the 'impact' of news on certain financial instruments
    - Definition of 'impact': how the publication of news affects/could affect certain financial instruments according to a certain level
    - Levels:
        * Global (country's economy) - if the news is about a state entity or about a company that makes up a significant share of GDP (or something similar)
        * Local (industry) - if the news is about the industry or about a major player within the industry, the influence of which can greatly affect the industry
        * Spot (company) - if the news is about a specific company
    - Financial indicators:
        * Global level: MOEX index, RVI index, RUBUSD rate
        * Local level: industry index (i.e. MOEXOG, MOEXEU, MOEXTL, etc.)
        * Spot level: shares of companies according to ticket (i.e. VKCO, SBER, YNDX, etc.)
    - Output models:
        * Tags: '+' - positive 'influence', '0' - no 'influence', '-' - negative 'influence'
* Creating a graph of connections between financial market entities
* Using GNN methods for: **TBA**
* Creating a Telegram bot
* Creating a FastApi service around models and data
* Creating a Streamlit service that interacts with the API

**Work plan:**
* Data collection
    - Sources:
        * Smart Lab
        * Kommersant
        * Ria
        * Interfax
    - Data store:
        * DVC (GDrive)
* List of tasks at the first stage (exploratory data analysis and primary data analysis):
    - Clean data from “empty” news (for example, there are news where there are only pictures or only a link to an external news)
    - Get rid of completely duplicate news
    - Clean the body of the news from uninformative parts (for example, repeated text, external links, etc.)
    - Look at the distribution of news text lengths relative to the portals where the news were taken and draw conclusions
    - Study the sections from which our news was taken
    - Construct a time series, where the x-axis is the date of the news, and the y-axis is the number of news on this date, study the profile of this time series
    - Get rid of news that was published outside of trading hours
* List of tasks at the second stage (classic ML + DL):
    - Extract necessary entities from news
    - Get rid of duplicate news ("duplicate news" mean news that repeats the meaning of an event in different words on different portals)
    - Using NLP methods, generate a label for the “impact” of news globally on the economy/locally on the relevant industry/specifically on a specific company
    - Make an MVP of the service
* List of tasks at the third stage (DL deep):
    - Additionally parse the data (since the initial ones were not enough)
    - Create a graph of connections between financial market entities
    - Apply some GNN methods
    - etc. (TBA)
* List of tasks at the fourth stage (service creation):
    - Create a Telegram bot, which receives a link to a news item from many “acceptable” portals as an input, and at the output the user receives aggregated information about the news
    - Make it possible to obtain information about the structure of the graph
* List of tasks that we want to do, but may not have time:
    - Expand sources of news (add news portals)
    - Organize additional training of the model: periodically additionally parse news, put them in the database, write a pipeline for additional training of the model (MLOps) and update the weights and graph structure of the model lying in the back of the Telegram bot

**Telegram-bot:** [tg-bot](https://t.me/project_news_anal_bot)

**FastAPI service:** <pufto, but it won’t be pufto>

**Streamlit mini-app:** <pufto, but it won’t be pufto>
