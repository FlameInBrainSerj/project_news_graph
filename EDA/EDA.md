# EDA

**Выводы:**
* URL   
    - Избавились от повторяющихся наблюдений (новостей)  
* Body   
    - Почистили тексты от неинформативных и ненужных частей, которые могли бы навредить качеству наших последующих моделей (избавились от повторяющихся частей у всех новостей и внешних ссылок)   
    - После чистики текстов новостей избавились от практически неинформативных (очень коротких) и дублирующихся (по тексту) новостей    
    - Заметили, что у нас распределение длин текстов новостей определеятся порталом, из которго новость была взята, на данный момент это не дает нам какой-то конкретной информации (кроме того, что у нас достаточно разношерстный корпусов текстов), но мы будем держать это в уме при последующем обучении моделей    
* Section    
    - Изначально была идея избавиться от новостей, которые не подходят под нашу тему на основе неподходящих секций, но, по итогу, решили, что неподходящие новости мы отсеем на этапе извлечения сущностей, так как новость в таком случае будет считаться неподходящей, если не содержит в себе нужную(ые) нам сущность(и). Как следствие, на данный момент никаких преобразований на основе информации о секции, из которой была взята новость, решили не делать   
* Date  
    - По временному ряду новостей видно, что количество новостей колеблется около среднего в примерно 160-170 новостей в день в дни, когда работает Московская биржа   
    - Есть отдельные сильные провалы, связанные с выходными днями по общему календарю, однако биржа в этот день работала, поэтому мы не исключали эти даты. Это начало января, 24 февраля и 8 мая
    - Есть и очень насыщенный день 15 июня. Вероятно, это связано с проведением ПМЭФ
    - В целом, ряд выглядит относительно стационарным, сезонности и трендов после исключения выходных и праздников не наблюдается
* Tags   
    - Большая часть ключевых слов встречается небольшое количество раз: от 1 до 3 раз встречаются 12000 тэгов и ключевых слов   
    - Скорее всего, редко встречаемые тэги не будут отражать никакие сущности, однако возможно среди них встречаются синонимы или части сущностей, которые отражены более встречающимися тэгами    
    - На этапе обработки данных мы попробуем извлечь словарь сущностей   
    - Наиболее встречающиеся ключевые слова тоже могут не являться сущностями    
* Итог
    - Запушили 'очищенный' датасет в новую таблицу в нашей базе данных   
