import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm.auto import tqdm


def parse_links_smart_lab(
    webdriver_options: Options,
    lst_dates: list[str],
) -> list[str | None]:
    """
    Parse links from Smart Lab according to certain dates.

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

        driver.get(f"https://smart-lab.ru/news/date/{date}")
        time.sleep(0.5)

        elements = driver.find_elements(
            By.XPATH,
            '//div[@class="topic allbloglist"]//h3//div[@class="inside"]//a',
        )
        for element in elements:
            lst_links.append(element.get_attribute("href"))

        try:
            # For each date there is no more than 2 pages
            next_page_btn = driver.find_element(By.XPATH, '//*[@id="pagination"]/a[2]')
            next_page_btn.click()
            time.sleep(1)
            elements = driver.find_elements(
                By.XPATH,
                '//div[@class="topic allbloglist"]//h3//div[@class="inside"]//a',
            )
            for element in elements:
                lst_links.append(element.get_attribute("href"))
        except BaseException:
            pass

    driver.close()
    driver.quit()

    return list(set(lst_links))


def parse_smart_lab_news_on_list_of_links_and_save(
    webdriver_options: Options,
    lst_links: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Smart Lab news by certain links.

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
    key_words_lst = []

    regex_for_external_links = (
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]"
        r"{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9"
        r"()@:%_\+.~#?&//=]*)"
    )

    driver = webdriver.Chrome(options=webdriver_options)

    for i in tqdm(range(len(lst_links))):

        # To dodge heap overflow error
        if i % 100 == 0 and i != 0:
            driver.close()
            driver.quit()

            driver = webdriver.Chrome(options=webdriver_options)

        try:
            driver.get(lst_links[i])
            time.sleep(0.2)

            # Body
            body = driver.find_element(
                By.XPATH,
                '//div[@id="content"]//div//div[@class="content"]',
            ).text
            body_without_external_links = re.sub(regex_for_external_links, "", body)
            if body_without_external_links.strip() == "":
                continue
            # Header
            header = driver.find_element(
                By.XPATH,
                '//div[@id="content"]//div//h1//span',
            ).text
            # Date
            news_date = driver.find_element(By.XPATH, '//li[@class="date"]').text
            # Keywords
            key_words_phrase = driver.find_element(By.XPATH, '//ul[@class="tags"]')
            key_words_paths = key_words_phrase.find_elements(By.XPATH, ".//li")
            key_words = [
                key_words_paths[i].text.replace(",", "")
                for i in range(1, len(key_words_paths))
            ]

            body_lst.append(body_without_external_links)
            header_lst.append(header)
            date_lst.append(news_date)
            key_words_lst.append(key_words)
            new_urls_lst.append(lst_links[i])

        except BaseException:
            pass

    driver.close()
    driver.quit()

    website_lst = ["Smart_Lab" for _ in range(len(body_lst))]
    section_lst = ["Новости компаний и новости по акциям" for _ in range(len(body_lst))]

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
        f"{data_dir_path}/smart_lab_{start_date}_{end_date}.parquet",
        index=False,
    )


def smart_lab_parse(
    options: Options,
    lst_dates: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Smart Lab.

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
    lst_links = parse_links_smart_lab(webdriver_options=options, lst_dates=lst_dates)

    parse_smart_lab_news_on_list_of_links_and_save(
        webdriver_options=options,
        lst_links=lst_links,
        data_dir_path=data_dir_path,
        start_date=start_date,
        end_date=end_date,
    )
