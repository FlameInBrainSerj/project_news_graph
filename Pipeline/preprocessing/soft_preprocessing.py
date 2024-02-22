import re

import pandas as pd
from utils import date_changer, date_ria_extract


def remove_duplicated_urls(df: pd.DataFrame) -> None:
    df.dropna(subset=["url"], inplace=True)


def remove_links_and_garbage(df: pd.DataFrame) -> None:
    links_patterns = [
        (
            r"(?:(?:https?|ftp):\/\/|www\.)[-A-Za-z0-9+&@#\/%?=~_|!:,.;]*"
            r"[-A-Za-z0-9+&@#\/%=~_|]"
        ),
        r"(?<=\s)fomag\.ru[^ ]*",
        r"(?<=\n|1)[^ ]*\.html",
        r"(?<=\n)[^ ]*\.pdf",
        r"(?<=\s)tass\.ru[^ ]*",
        r"(?<=\s)t.me[^ ]*",
    ]
    garbage_patterns = [
        r"^.*(?:—|-|–) РИА Новости(?:.|,)",
        r"^.*INTERFAX.RU",
        r"\\nФото.*?\\n",
        r"\\n([А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*).{0,120}$",
        r"\\nЕще больше новостей в Telegram-канале «Коммерсантъ»[.]",
        r"Интервью взял.*",
        r"(Подробн.{2,4}|О) .*(«Ъ»|“Ъ”|материале|публикации).*$",
    ]

    for i in range(df.shape[0]):
        text = df.loc[i, "body"]
        if text is not None:
            for pattern in links_patterns + garbage_patterns:
                text = re.sub(pattern, " ", text)
        df.loc[i, "body"] = text


def remove_short_news(df: pd.DataFrame) -> None:
    # Get distribution of lengths in sample
    df.loc[:, "body_length"] = df["body"].apply(len)
    # Get length by 0.04 quantile
    length = df[["body_length"]].quantile(0.04).iloc[0]
    # Drop news of length shorter than 0.04 quantile
    df.drop(df[df["body_length"] < length].index, inplace=True)
    df.reset_index(drop=True, inplace=True)


def dates_preprocess(df: pd.DataFrame) -> None:
    df_ria = df[df["website"] == "РИА"]
    ria_dates = date_ria_extract(df_ria)

    for i in df.index:
        website = df.loc[i, "website"]

        if website == "Интерфакс":
            df.loc[i, "datetime"] = date_changer(
                date=df.date[i],
                convert_month=True,
                pattern="%H:%M, %d %m %Y",
            )
        if website == "Smart_Lab":
            df.loc[i, "datetime"] = date_changer(
                date=df.date[i],
                convert_month=True,
                pattern="%d %m %Y, %H:%M",
            )
        if website == "Kommersant":
            df.loc[i, "datetime"] = date_changer(
                date=df.date[i],
                convert_month=False,
                pattern="%d.%m.%Y, %H:%M",
            )

    for i, index in enumerate(df_ria.index):
        df.loc[index, "datetime"] = date_changer(
            date=ria_dates[i],
            convert_month=False,
            pattern="%H:%M %d.%m.%Y",
        )

    df.drop(["date"], axis=1, inplace=True)


def soft_preprocess(df: pd.DataFrame) -> None:
    remove_duplicated_urls(df)
    remove_links_and_garbage(df)
    remove_short_news(df)
    dates_preprocess(df)
