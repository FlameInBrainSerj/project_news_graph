# Pipeline

**Pipeline stages:**
- **Data scraping:**
    - Sources: Ria, Smart-Lab, Interfax, Kommersant
    - Automated new data parsing with DAG: **TBA**
- **Data preprocessing:**
    - Soft preprocessing: removing duplicated news, removing links and garbage in the texts, removing short news, normalizing the datetimes of the news
    - Texts normalization: lowercasing the text, removing some excessive syntax, deleting stopwords, lemmatizing the texts
    - NER: financial named entities recognition
    - Trade data injection: injecting trading data in correspondence with named entities and datetime of the news
    - Creation of new datasets: creating three separate datasets (companies, industries, global)
- **Models' train and inference:**
    - Main framework: Pytorch Lightning
    - Experiments logging: **TBA**

**Scripts configuration:**

All the scripts are working with the configuration files in configs folder. If one wants to configure the work of Pipeline, these files should be configured. For detailed information of the configs check out the corresponding folder

**Makefile commands:**
```
# Running data scrapping (and selenium in Docker)
make run-scrapers

# Running data preprocessing
make run-preprocessing

# Running models' train
make run-model-train

# Running models' inference
make run-model-inference

# Running all 4 commands
make run-pipeline
```
