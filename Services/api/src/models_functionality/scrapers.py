import pandas as pd
from config import SELENIUM_HOST
from fastapi import HTTPException
from models_functionality.utils import WEBSITES_XPATHS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Options for webdriver
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

# Initialize webdriver
driver = webdriver.Remote(
    command_executor=f"http://{SELENIUM_HOST}:4444/wd/hub",
    options=options,
)


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
            [el.text for el in driver.find_elements(By.XPATH, WEBSITES_XPATHS[site])],
        )

        return body

    except Exception:
        raise HTTPException(
            "Sorry, some webpages were not parsed, please, try one more time",
        )


def parse_links(links: pd.DataFrame) -> pd.DataFrame:
    """
    Parse bodies of the news by the links.

    :param links: dataframe with links
    :type links: pd.DataFrame

    :rtype: pd.DataFrame
    :return texts: dataframe with the texts
    """
    texts = []

    for url in links.iloc[:, 0].values:
        text = ""
        # Identifying whether we can parse the website by certain url
        for site in WEBSITES_XPATHS.keys():
            if site in url:
                text = parse_page(url, site)

        if len(text):
            texts.append(text)

        else:
            raise HTTPException(
                status_code=403,
                detail="Sorry, but some webpages were not parsed, because this "
                "service cannot parse such news portals or some pages were "
                "not loaded correctly, try one more time",
            )
    texts = pd.DataFrame({"Text": texts}, index=[i for i in range(links.shape[0])])

    return texts
