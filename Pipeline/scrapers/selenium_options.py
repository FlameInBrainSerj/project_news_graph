from selenium.webdriver.chrome.options import Options


def options_init() -> Options:
    """
    Initialize webdriver options.
    """
    # Scraper's options
    options = Options()

    # Fully load the page to avoid some problems
    options.page_load_strategy = "normal"

    # To avoid scraper detection and other problems
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    options.add_argument("--memory-alloc-policy=high")
    options.add_argument("--unlimited-storage")

    options.add_argument("--incognito")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disk-cache-size=0")
    options.add_argument("--disk-cache-dir=/dev/null")

    options.add_argument("--disable-notifications")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    return options
