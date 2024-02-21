# EDA

**Conclusions:**
* URL
    - No duplicated observations were found (news)
* Body
    - We cleaned the texts from uninformative and unnecessary parts that could harm the quality of our subsequent models (we got rid of repeating parts from all news and external links)
    - After cleaning the news texts, we got rid of practically uninformative (very short) and duplicative (in text) news
    - We noticed that our distribution of lengths of the news texts is determined by the portal where the news were taken, at the moment this does not give us any specific information (except that we have quite a varied corpus of texts), but we will keep this in mind during subsequent training of the models
* Section
    - Initially, there was an idea to get rid of news that did not fit our topic based on inappropriate sections, but, as a result, we decided that we would weed out inappropriate news at the named entity recognition (NER) stage, since the news in this case would be considered inappropriate if it does not contain the entity(ies) we need. As a result, at the moment, we decided not to make any transformations based on information about the section from which the news was taken
* Date
    - The time series of the news shows that the number of news has been fluctuating around the average of approximately 160-170 news per day on days when the Moscow Exchange is open since 2022. Before that it had been around 100-120 news
    - There are some strong dips associated with weekends according to the general calendar, but the exchange was working on that day, so we did not exclude these dates. These are holidays of January, February, May.
    - There is also a very busy day on June every year. This is probably due to the SPIEF
* Tags
    - Most of the keywords occur a small number of times: 27,000 tags and keywords occur 1 to 3 times
    - Most likely, rarely encountered tags will not reflect any entities, but perhaps among them there are synonyms or parts of entities that are reflected by more frequently occurring tags
    - At the data processing stage, we will try to extract a dictionary of entities
    - The most common keywords may also not be entities
* Summary
    - Pushed the 'cleaned' dataset into a new table in our database
