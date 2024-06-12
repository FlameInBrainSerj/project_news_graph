import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm.auto import tqdm


def parse_links_kommersant(
    webdriver_options: Options,
    lst_dates: list[str],
) -> list[str | None]:
    """
    Parse links from Kommersant according to certain dates.

    :param webdriver_options: webdriver options
    :type webdriver_options: Options
    :param lst_dates: list of dates associated with the news
    :type lst_dates: list[str]

    :rtype: list[str | None]
    :return list(set(lst_links)): list of unique news
    """
    lst_links = []
    driver = webdriver.Remote("http://localhost:4444/wd/hub", options=webdriver_options)

    for _, date in enumerate(lst_dates):
        driver.get(f"https://www.kommersant.ru/archive/rubric/40/day/{date}")

        elements = driver.find_elements(
            By.XPATH,
            '//div[@class="rubric_lenta"]//div//h2//a',
        )
        for element in elements:
            lst_links.append(element.get_attribute("href"))

    driver.close()
    driver.quit()

    return list(set(lst_links))


def parse_kommersant_news_on_list_of_links_and_save(
    webdriver_options: Options,
    lst_links: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Kommersant news by certain links.

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

    regex_for_external_links = (
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]"
        r"{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9"
        r"()@:%_\+.~#?&//=]*)"
    )

    driver = webdriver.Remote("http://localhost:4444/wd/hub", options=webdriver_options)

    for i in tqdm(range(len(lst_links)), desc="Parse Kommersant links"):

        # To dodge heap overflow error
        if i % 100 == 0 and i != 0:
            driver.close()
            driver.quit()

            driver = webdriver.Remote(
                "http://localhost:4444/wd/hub",
                options=webdriver_options,
            )

        try:
            driver.get(lst_links[i])
            time.sleep(0.2)

            # Body
            body = driver.find_element(
                By.XPATH,
                '//div[@class="doc__body"]/div[2]',
            ).text
            body_without_external_links = re.sub(regex_for_external_links, "", body)
            if body_without_external_links.strip() == "":
                continue
            # Header
            header = driver.find_element(
                By.XPATH,
                "//header/h1",
            ).text
            # Date
            date = driver.find_element(
                By.XPATH,
                '//div[@class="doc_header__time"]//time',
            ).text
            # Section
            section = driver.find_element(By.XPATH, '//ul[@class="crumbs"]//li//a').text

            body_lst.append(body_without_external_links)
            header_lst.append(header)
            date_lst.append(date)
            section_lst.append(section)
            new_urls_lst.append(lst_links[i])

        except BaseException:
            pass

    driver.close()
    driver.quit()

    website_lst = ["Kommersant" for _ in range(len(body_lst))]
    key_words_lst: list[list] = [[] for _ in range(len(body_lst))]

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
        f"{data_dir_path}/{start_date}_{end_date}/kommersant.parquet",
        index=False,
    )


def kommersant_parse(
    options: Options,
    lst_dates: list[str],
    data_dir_path: str,
    start_date: str,
    end_date: str,
) -> None:
    """
    Parse Kommersant.

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
    lst_links = parse_links_kommersant(webdriver_options=options, lst_dates=lst_dates)
    parse_kommersant_news_on_list_of_links_and_save(
        webdriver_options=options,
        lst_links=lst_links,
        data_dir_path=data_dir_path,
        start_date=start_date,
        end_date=end_date,
    )
