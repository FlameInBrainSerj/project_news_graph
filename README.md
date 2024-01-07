# Построение новостного графа и сервисов вокруг него


**Куратор:** Бабынин Андрей (@maninoffice)  
**Список членов команды:** Думенков Максим (@maxodum), Кривошеев Сергей (@FlameInBrain)  

**Описание проекта:** Парсинг новостей, их анализ методами NLP и GNN и создание сервисов вокруг полученных моделей, а именно:
* Создание NLP моделей, которые оценивают 'влияние' новости на определенные финансовые инструменты 
  - Опредление 'влияния': как выхож новости сказывается/может сказаться на опредленных финансовых инструментах согласно определенномк уровню
  - Уровни:
    * Глобальный (экономика страны) - если новость о государственной сущности или о компании, которая составляет серьезную долю в ВВП (или чем-то подобном)
    * Локальный (отрасль) - если новость об отрасли или о крупном игроке в рамках отрасли, влияние на которого может сильно повлиять на отрасль
    * Точечный (компания) - если новость о конкретной компании
  - Финансовые показатели:
    * Глобальный уровень: индекс MOEX, индекс RVI, курс RUBUSD
    * Локальный уровень: отраслевой индекс (i.e. MOEXOG, MOEXEU, MOEXTL, etc.)
    * Точечный уровень: акции компаний согласно тикету (i.e. VKCO, SBER, YNDX, etc.)
  - Output модели: 
    * Метки: '+' - положительное 'влияние', '0' - отсутствие 'влияния', '-' - отрицательное 'влияние'
* Создание графа связей сущностей финансового рынка 
* Использование методов GNN для: <TBA>
* Создание Telegram-бота
* Создание FastApi сервиса вокруг моделей и данных
* Создание Streamlit сервиса, взаимодействующего с API 

**План работы:**
* Сбор данных
  - Источники:
    * Smart Lab
    * Коммерсант
    * РИА
    * Интерфакс
  - Хранилище данных: 
    * Postgresql   
* Список задач на первом этапе (разведочный анализ данных и первичная аналитика данных):   
  - Почистить данные от "пустых" новостей (например, есть новости, где есть только картинки или только ссылка на внешнюю новость)    
  - Избавиться от полностью дублирующихся новостей   
  - Почистить body новостей от неинформативных частей     (например, от всюду повторяющегося текста, внешних ссылок и т.д.)    
  - Посмотреть на распределение длин текстов новостей относительно порталов, откуда были взяты новостей и сделать выводы   
  - Изучить секции, из которых у нас были взяты новости   
  - Построить временной ряд, где по оси абсцисс - дата новости, а по оси ординат - количество новостей в эту дату, изучить профиль этого временного ряда   
  - Избавиться от новостей, которые были опубликованы в нерабочее время для бирж    
* Список задач на втором этапе (classic ML + DL):
  - Извлечь необходимые сущности из новостей   
  - Избавиться от новостей дубликатов (под дубликатами подразумеваются новости повторяющие смысл произошедшего события разные словами на разных порталах)   
  - Методами NLP сгенерировать маркировку на предмет "влияния" новости глобально на экономику/локально на соответствующую отрасль/точечно на конкретную компанию 
  - Сделать MVP сервиса   
* Список задач на третьем этапе (DL deep):
  - Дополнительно спарсить данные (т.к. не хватило изначальных)
  - Сделать граф связей сущностей финансового рынка 
  - Применить какие-нибудь методы GNN
  - и т.д. (TBA)
* Список задач на четвертом этапе (создание сервиса):
  - Создать Telegram-бота, которому на вход подается ссылка на новость из множества "допустимых" порталов, а на выходе пользователь получает аггрегированную информацию о новости
  - Сделать возможным получать информацию о структуре графа
* Список задач, которые хочется сделать, но возможно не успеем:
  - Расширить источники получения новостей (добавить новостные порталы)    
  - Организовать дообучаемость модели: периодично дополнительно парсить новости, класть их в БД, написать пайплайн для дообучения модели (MLOps) и обновлять веса и структуру графа модели, лежащей в бэке Telegram-бота    

**Ссылка на Telegram-бота:** <пуфто, но будет не пуфто>   
**Ссылка на FastAPI сервис:** <пуфто, но будет не пуфто>   
**Ссылка на Streamlit мини-приложение:** <пуфто, но будет не пуфто>   

**GIF работы сервиса:** <пуфто, но будет не пуфто>   
