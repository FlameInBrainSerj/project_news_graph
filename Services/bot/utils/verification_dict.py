available_scores = ["1", "2", "3", "4", "5"]

WEBSITES_XPATHS = {
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
