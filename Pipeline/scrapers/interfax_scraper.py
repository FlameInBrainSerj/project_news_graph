import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm.auto import tqdm


def parse_links_interfax(
    webdriver_options: Options,
    lst_dates: list[str],
) -> list[str | None]:
    """
    Parse links from Interfax according to certain dates.

    :param webdriver_options: webdriver options
    :type webdriver_options: Options
    :param lst_dates: list of dates associated with the news
    :type lst_dates: list[str]

    :rtype: list[str | None]
    :return list(set(lst_links)): list of unique news
    """
    lst_links = []
    driver = webdriver.Chrome(options=webdriver_options)

    for _, date in enumerate(lst_dates):
        driver.get(f"https://www.interfax.ru/business/news/{date}")
        time.sleep(1)

        elements = driver.find_elements(By.XPATH, "//div[@class='an']/div/a")
        for element in elements:
            lst_links.append(element.get_attribute("href"))

    driver.close()
    driver.quit()

    return list(set(lst_links))


def parse_interfax_news_on_list_of_links_and_save(
    webdriver_options: Options,
    lst_links: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Interfax news by certain links.

    :param webdriver_options: webdriver options
    :type webdriver_options: Options
    :param lst_links: list of links
    :type lst_links: list[str]
    :param data_dir_path: path where to store parsed data
    :type data_dir_path: str
    :param start_date: starting date of time span
    :type start_date: str
    :param end_date: ending date of time span
    :type end_date: str
    """
    new_urls_lst = []
    body_lst = []
    header_lst = []
    date_lst = []
    section_lst = []
    key_words_lst = []

    driver = webdriver.Chrome(options=webdriver_options)

    for i in tqdm(range(len(lst_links)), desc="Parse Interfax links"):

        # To dodge heap overflow error
        if i % 100 == 0 and i != 0:
            driver.close()
            driver.quit()

            driver = webdriver.Chrome(options=webdriver_options)

        try:
            driver.get(lst_links[i])
            time.sleep(0.2)

            # Body
            paragraphs = driver.find_elements(
                By.XPATH,
                '//article[@itemprop="articleBody"]/p',
            )
            body = "\n".join([p.text for p in paragraphs])
            # Header
            header = driver.find_element(
                By.XPATH,
                '//article[@itemprop="articleBody"]/h1',
            ).text
            # Date
            date = driver.find_element(By.XPATH, "//time").text
            # Section
            section = driver.find_element(
                By.XPATH,
                "/html/body/main/div[1]/div/div/aside/a",
            ).text
            # Keywords
            try:
                tags = driver.find_element(
                    By.XPATH,
                    '//div[@class="textMTags"]',
                )
                key_words = tags.text.split("\n")
            except NoSuchElementException:
                key_words = []

            body_lst.append(body)
            header_lst.append(header)
            date_lst.append(date)
            section_lst.append(section)
            key_words_lst.append(key_words)
            new_urls_lst.append(lst_links[i])

        except BaseException:
            pass

    driver.close()
    driver.quit()

    website_lst = ["Интерфакс" for _ in range(len(body_lst))]

    df = pd.DataFrame(
        {
            "website": website_lst,
            "section": section_lst,
            "url": new_urls_lst,
            "header": header_lst,
            "body": body_lst,
            "date": date_lst,
            "key_words": key_words_lst,
        },
    )

    df.to_parquet(
        f"{data_dir_path}/{start_date}_{end_date}/interfax.parquet",
        index=False,
    )


def interfax_parse(
    options: Options,
    lst_dates: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Interfax.

    :param options: webdriver options
    :type options: Options
    :param lst_dates: list of dates associated with the news
    :type lst_dates: list[str]
    :param data_dir_path: path where to store parsed data
    :type data_dir_path: str
    :param start_date: starting date of time span
    :type start_date: str
    :param end_date: ending date of time span
    :type end_date: str
    """
    lst_links = parse_links_interfax(webdriver_options=options, lst_dates=lst_dates)
    parse_interfax_news_on_list_of_links_and_save(
        webdriver_options=options,
        lst_links=lst_links,
        data_dir_path=data_dir_path,
        start_date=start_date,
        end_date=end_date,
    )
