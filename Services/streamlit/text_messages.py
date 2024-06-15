TAB1_INTERFAX = """Most of the drop in the number of news coincides with weekends and holidays on which the exchange 
was not open. The average number of news items was approximately 25-30 before 2022. Since 2022 it has been at level 
of 75 news per day. Variance also increased."""

TAB1_RIA = """Most of the drop in the number of news coincides with weekends and holidays on which the 
                exchange was not open. The average number of news items was approximately 50 in 2019, 2021, 2023. In 2020 
                and 2022 there were gaps in the beginning of year and consequent reggression to average."""

TAB1_SMART_LAB = """Most of the drop in the number of news coincides with weekends and holidays on which the 
                exchange was not open. The average number of news items has been approximately 70 since 2022. Before 2022 
                it had been around 40 news per day in average. It deviates from other sources in that there are many 
                other dips in the number of news items. Possible reason: the nature of the portal itself, aggregation of 
                news with lags."""

TAB1_KOMMERSANT = """Most of the drop in the number of news coincides with weekends and holidays on which the 
                exchange was not open. The average number of news items is approximately 12-13."""

TAB1_TOTAL = """The general time series looks like a mixture of Interfax and RIA due to the amount of news 
                from these publications. In the overall picture, a decrease in the number of news events even more often 
                coincides with non-working days for the stock exchange. Increase in average number of news and variance 
                is also present in general time series."""

TAB1_LENGTH = """You can notice that our distribution of lengths of news texts is determined by the website from 
which the news was taken, at the moment this does not give us any specific information (except that we have a fairly 
diverse corpus of texts), but we will keep this in mind when training models later"""

TAB2_WEBSITE = (
    "If we take news without duplicates, we get the following picture: Kommersant takes the last place in "
    "terms of the number of news presented, Interfax and RIA are approximately close, and their gap narrows"
    "when duplicates are removed (Interfax news, apparently, more often covers several companies at once), "
    "and the leader turns out to be a Smart lab that aggregates news and with other portals"
)

TAB3_WEBSITE = (
    "If we take news without duplicates, we get the following picture: Kommersant takes the last place in "
    "terms of the number of news presented, Interfax and RIA are approximately close, and their gap narrows"
    " when duplicates are removed (Interfax news, apparently, more often covers several industries at "
    "once), and the leader turns out to be a Smart lab that aggregates news and with other portals"
)

TAB4_WEBSITE = (
    "Kommersant takes the last place in "
    "terms of the number of news presented, Interfax and Smart lab are approximately close,"
    " and RIA creates the most of news"
)

TAB2_SECTION = (
    "The most popular sections:\n\n"
    '"Economics" and "Company News and Stock News" are the two most popular '
    "sections, each of which contains about 20 thousand news items.These two sections are significantly "
    "ahead of the others in terms of the number of news.\n\n"
    '"In Russia" section is explainable by our topic of interest.\n\n'
    "Interesting that one of companies has mention in section of some website"
)

TAB3_SECTION = (
    "The most popular sections:\n\n"
    '"Economics" and "Company News and Stock News" are the two most popular '
    "sections, each of which contains about 20 thousand news items.These two sections are significantly "
    "ahead of the others in terms of the number of news.\n\n"
    '"In Russia" section is explainable by our topic of interest.\n\n'
    "Interesting that one of companies has mention in section of some website"
)

TAB4_SECTION = (
    "The most popular sections:\n\n"
    '"Economics" and "Company News and Stock News" are the two most popular '
    "sections, each of which contains about 20 thousand news items.These two sections are significantly "
    "ahead of the others in terms of the number of news.\n\n"
    '"In Russia" section is explainable by our topic of interest.\n\n'
    'There is also a difference compared to other datasets: "exchange rate and oil prices" section appears.'
)

TAB2_HEADER = (
    "Average headline length:\n\n"
    "Most headlines are between 50 and 100 characters long, indicating a "
    "preference for shorter and more concise headlines.\n\n"
    "Distribution peak:\n\n"
    "The largest number of "
    "headings (approximately 8000) is about 75 characters long. This may be the optimal length for the "
    "title so that it is informative enough, but not too long.\n\n"
    "Length range:\n\n"
    "The headings range from "
    "very short (less than 25 characters) to very long (up to 200 characters), but there are much fewer "
    "such headings."
)

TAB3_HEADER = (
    "Average headline length:\n\n"
    "Most headlines are between 50 and 100 characters long, indicating a "
    "preference for shorter and more concise headlines.\n\n"
    "Distribution peak:\n\n"
    "The largest number of "
    "headings (approximately 8000) is about 75 characters long. This may be the optimal length for the "
    "title so that it is informative enough, but not too long.\n\n"
    "Length range:\n\n"
    "The headings range from "
    "very short (less than 25 characters) to very long (up to 200 characters), but there are much fewer "
    "such headings."
)

TAB4_HEADER = (
    "Average headline length:\n\n"
    "Most headlines are between 50 and 100 characters long, indicating a "
    "preference for shorter and more concise headlines.\n\n"
    "Distribution peak:\n\n"
    "The largest number of "
    "headings (approximately 8000) is about 75 characters long. This may be the optimal length for the "
    "title so that it is informative enough, but not too long.\n\n"
    "Length range:\n\n"
    "The headings range from "
    "very short (less than 25 characters) to very long (up to 200 characters), but there are much fewer "
    "such headings."
)

TAB2_BODY = (
    "General distribution:\n\n"
    "Most texts are between 0 and 2000 characters long for all four websites. "
    "After 2000 characters, the number of texts decreases dramatically, although there are texts up to "
    "10,000 characters long.\n\n"
    "Comparison between websites:\n\n"
    "Kommersant and Ria have a similar "
    "distribution, with the largest number of texts of about 1000 characters. Interfax shows a "
    "slightly different picture, with a lot of longer texts, but also having a peak of about "
    "1000-1500 characters. Smart Lab has more texts in the range of 500-1500 characters, "
    "but then the number of texts decreases faster as the length of the text increases compared to "
    "other sites.\n\n"
    "Characteristics of the texts:\n\n"
    "Smart Lab and Ria tend to publish shorter texts "
    "compared to Interfax, which seems to include more long articles. Kommersant also has relatively "
    "short texts, but there are more medium-length texts (up to 2000 characters) in their "
    "distribution.\n\n"
    "Text length:\n\n"
    "All sites have texts up to 10,000 characters long, although there "
    "are significantly fewer such texts. The distribution peaks for all sites range from 500 to 2000 "
    "characters, which may indicate the optimal text length for news.\n\n"
)

TAB2_BODY_DATE = (
    "Length of texts over time:\n\n"
    "The average length of news per day does not change over time, "
    "but there are individual peaks in December, which can most likely be explained by news that "
    "summarizes the stories that took place in the past year"
)

TAB3_BODY = (
    "General distribution:\n\n"
    "Most texts are between 0 and 2000 characters long for all four websites. "
    "After 2000 characters, the number of texts decreases dramatically, although there are texts up to "
    "10,000 characters long.\n\n"
    "Comparison between websites:\n\n"
    "Interfax and Ria have a similar "
    "distribution, with the largest number of texts of about 1000 characters. Interfax shows a "
    "slightly different picture, with a lot of longer texts, but also having a peak of about "
    "1000-1500 characters.\n\n"
    "Characteristics of the texts:\n\n"
    "Smart Lab and Ria tend to publish shorter texts "
    "compared to Interfax, which seems to include more long articles. Kommersant also has relatively "
    "short texts, but there are more medium-length texts (up to 2000 characters) in their "
    "distribution.\n\n"
    "Text length:\n\n"
    "All sites have texts up to 10,000 characters long, although there "
    "are significantly fewer such texts. The distribution peaks for all sites range from 500 to 2000 "
    "characters, which may indicate the optimal text length for news.\n\n"
)

TAB3_BODY_DATE = (
    "Length of texts over time:\n\n"
    "The average length of news per day does not change over time, "
    "but there are individual peaks in December, which can most likely be explained by news that "
    "summarizes the stories that took place in the past year"
)

TAB4_BODY = (
    "General distribution:\n\n"
    "Most texts are between 0 and 2000 characters long for all four websites. "
    "After 2000 characters, the number of texts decreases dramatically, although there are texts up to "
    "10,000 characters long.\n\n"
    "Comparison between websites:\n\n"
    "Kommersant and Ria have a similar "
    "distribution, with the largest number of texts of about 1000 characters. Interfax shows a "
    "slightly different picture, with a lot of longer texts, but also having a peak of about "
    "1000-1500 characters. Smart Lab has more texts in the range of 500-1500 characters, "
    "but then the number of texts decreases faster as the length of the text increases compared to "
    "other sites.\n\n"
    "Characteristics of the texts:\n\n"
    "Smart Lab and Ria tend to publish shorter texts "
    "compared to Interfax, which seems to include more long articles. Kommersant also has relatively "
    "short texts, but there are more medium-length texts (up to 2000 characters) in their "
    "distribution.\n\n"
    "Text length:\n\n"
    "All sites have texts up to 10,000 characters long, although there "
    "are significantly fewer such texts. The distribution peaks for all sites range from 500 to 2000 "
    "characters, which may indicate the optimal text length for news.\n\n"
)

TAB4_BODY_DATE = (
    "Length of texts over time:\n\n"
    "The average length of news per day does not change over time, "
    "but there are individual peaks in December, which can most likely be explained by news that "
    "summarizes the stories that took place in the past year. There is a huge spike in May 21."
)

TAB2_KEY_WORDS = (
    'The most common tags for stocks are "stocks" and "economics". There are several companies among '
    "the tags, and they"
    "have the most news. "
)

TAB3_KEY_WORDS = (
    "The most common tags for stocks are stocks. There are several companies among the tags, and they "
    "had the most news. Novatek and the Northern stream are important for industries, but not for "
    "stocks."
)

TAB4_KEY_WORDS = (
    'The most common tags for global are "economics", "Russia" and "stocks". There are two main '
    "speakers in Russian economy: Putin and Mishustin. Also Central Bank is stated among popular tags"
)

TAB2_COMPANY = (
    "3 companies stand out from the rest by the number of mentions in news texts: These are Gazprom, "
    "Sberbank and VTB. They are found in from 8 to 4 thousand news. The rest are found in no more than 2 "
    "each"
)

TAB3_INDUSTRY = (
    "2 industries are distinguished by the amount of news: oil and gas and financial. They generate more "
    "than 10 thousand news each. The least news about the chemical industry is just over 500."
)

TAB2_DATE = (
    "The number of news items on the date looks relatively steady, with a slight increase at the junction of "
    "the 21st and 22nd years. There are also peaks coinciding with the SPIEF and the announcements of "
    "sanctions"
)

TAB3_DATE = (
    "Mean of this time series doesn't seem to change, but there is a slight rise in the first half of 2022. "
    "This timeseries is highly volatile."
)

TAB4_DATE = (
    "The number of news items on the date looks relatively steady, with a slight rise in the first half of "
    "2022. There are also peaks coinciding with the SPIEF and the announcements of"
    "sanctions. Down peaks are associated with nearest holidays"
)

TAB2_TRADING = (
    "The yield hovers around zero half an hour after the news is released."
    "Until 2022, it was less volatile than in subsequent periods. "
    "Volatility peaked in the first half of 2022."
)

TAB3_TRADING = (
    "The yield hovers around zero half an hour after the news is released. "
    "This time series looks relatively still compared to the stock returns. "
    "Volatility peakes in the first half of 2022."
)

TAB4_TRADING_IMOEX = (
    "The yield hovers around zero half an hour after the news is released."
    "This time series looks relatively still compared to the stock returns."
    "Volatility peaks in the first half of 2022."
)

TAB4_TRADING_RVI = (
    "The yield hovers around zero. Volatility raised in 2022 and stood high afterwords. Number of "
    "peaks had been higher after since 2022. Volatility peaked in the first half of 2022."
)

TAB4_TRADING_USD = (
    "The yield hovers around zero. Volatility peaked in the first half of 2022."
    " There are much more deep sharp declines than rises"
)

TAB5 = (
    "1. Clusters are distributed very similarly to industries, while some clusters have connections, and some do "
    "not.\n\n"
    "2. The graph can be divided into 2 halves, in the first of which the companies of the consumer segment, "
    "and in the second - mining and processing.\n\n"
    "3. Within the cluster, the bonds can be stronger (both in metals) and weaker (IT).\n\n"
    "4. Ownership relationships have been caught (MTSS and ETLN partially belong to AFKS).\n\n"
)
