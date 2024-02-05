import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils.custom_exceptions import ParseError
from utils.text_messages import ERROR_MSG_PAGE_NOT_LOADED

websites_xpath = {
    # Stable
    "smart-lab": "//div[@id='content']//div//div[@class='content']",
    "interfax": "//article[@itemprop='articleBody']",
    "kommersant": "//div[@class='doc__body']/div[2]",
    "ria": "//div[@class='layout-article__main-over']/div[1]/div[3]"
    "/div[@data-type='text' or @data-type='quote']",
    # OK
    "rbc": "//div[@itemprop='articleBody']/p",
    "lenta": "//main/div[2]/div[3]/div[1]/div[2]/div[1]",
    "gazeta": "//div[@itemprop='articleBody']/p",
    "tass": "//article",
    "iz.ru": "//div[@itemprop='articleBody']/div/p",
    # Unstable
    "finam": "/html/body/div[1]/div/div[2]/div/div[5]/div[1]/div[3]/div[2]/p",
}


def initialize_webdriver_options() -> Options:
    """
    Initialize webdriver options for parsing.

    :rtype: Options
    :return options: options for webdriver
    """
    options = Options()

    options.page_load_strategy = "eager"
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    return options


webdriver_options = initialize_webdriver_options()


def initialize_webdriver(webdriver_options: Options = webdriver_options) -> None:
    """
    Initialize webdriver.

    :param webdriver_options: options for webdriver
    :type webdriver_options: Options
    """
    global driver
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options=webdriver_options)


initialize_webdriver()


def parse_page(
    url: str,
    site: str,
) -> str:
    """
    Parse news' page.

    :param url: url of the news
    :type url: str
    :param site: portal where news is published
    :type site: str

    :rtype: str
    :return body: body of the news
    """
    try:
        driver.get(url)
        body = " ".join(
            [el.text for el in driver.find_elements(By.XPATH, websites_xpath[site])],
        )

        # Raise error when page was not parsed because it has not fully loaded
        if len(body) == 0:
            raise ParseError(
                ERROR_MSG_PAGE_NOT_LOADED,
            )

        return body
    except Exception as e:
        logging.error(e)
        raise ParseError("Sorry, the page was not parsed :(, please, try another link")
