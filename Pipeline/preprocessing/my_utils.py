import re
from datetime import date, datetime

import pandas as pd

companies = {
    # One
    "SBER": r"\s(?:сбербанк|сбер|sber|sberbank)\s",
    "LKOH": r"\s(:?лукойл|lukoil|lkoh)\s",
    "GAZP": r"\s(:?газпром|gazprom|gazp)\s",
    "GMKN": r"\s(:?норильский никель|норникель|gmkn|nornikel|гмкнорник|норник)\s",
    "NVTK": r"\s(:?новатэк|novatek|nvtk)\s",
    "YNDX": r"\s(:?яндекс|yandex|yndx|янд)\s",
    "ROSN": r"\s(:?роснефть|rosn|rosneft)\s",
    "TATN": r"\s(:?татнефть|татнфт|tatn|tatneft)\s",
    "MGNT": r"\s(:?магнит|mgnt|magnit)\s",
    "TCSG": r"\s(:?tcg|tcs|tcsg|тиньк|тинькофф|тиньков)\s",
    # Two
    "SNGS": r"\s(:?сургутнефтегаз|сургнфгз|sngs|surgutneftegas)\s",
    "TRNF": r"\s(:?транснефть|транснф|trnf|transneft)\s",
    "PLZL": r"\s(:?полюс|plzl|polus zoloto|polus)\s",
    "CHMF": r"\s(:?северсталь|севст|chmf|severstal)\s",
    "FIVE": r"\s(:?x5|five)\s",
    "NLMK": r"\s(:?нлмк|nlmk|новолипецкий металлургический комбинат|новолипецкий)\s",
    "MTSS": r"\s(:?мтс|мобильные телесистемы|mts|mtss)\s",
    # Three
    "PHOR": r"\s(:?фосагро|phor|phosagro)\s",
    "POLY": r"\s(:?полиметалл|polymetal|poly)\s",
    "ALRS": r"\s(:?алроса|alrs|alrosa)\s",
    "IRAO": r"\s(:?интеррао|интер рао|irao|inter rao|interrao)\s",
    "OZON": r"\s(:?ozon|озон)\s",
    "MAGN": r"\s(:?магнитогорский металлургический комбинат|ммк|magn|mmk)\s",
    "VTBR": r"\s(:?втб|vtb|vtbr)\s",
    "HHRU": r"\s(:?headhunter|hh|hhru|хэдхантер|хэдхантэр)\s",
    "RUAL": r"\s(:?русал|rusal|rual)\s",
    "PIKK": r"\s(:?пик|pikk|pik)\s",
    # Four
    "ENPG": r"\s(:?эн\+ груп|en\+ group|эн\+|en\+|эн\+груп|enpg|en\+group)\s",
    "RTKM": r"\s(:?ростелеком|ростел|rostel|rostelecom|rtkm)\s",
    "MTLR": r"\s(:?мечел|mechel|mltr)\s",
    "FIXP": r"\s(:?fix|fix price|fixp|фикс прайс)\s",
    "GLTR": r"\s(:?globaltrans|gltr|глобалтранс|global trans|глобал транс)\s",
    "CBOM": r"\s(:?московский кредитный банк|мкб|mkb|московский банк|cbom)\s",
    "HYDR": r"\s(:?русгидро|hydr|rushydro)\s",
    "AGRO": r"\s(:?русагро|agro|rusagro)\s",
    "AFKS": r"\s(:?афк система|афк|afks|afk|afk system)\s",
    # Five
    "BANE": r"\s(:?башнефт|башнефть|bane|bashneft)\s",
    "KAZT": r"\s(:?куйбазот|куйбышевазот|kazt)\s",
    "FLOT": r"\s(:?совкомфлот|sovkomflot|flot)\s",
    "FEES": r"\s(:?фск россети|fees|fsk rosseti)\s",
    "VSMO": r"\s(:?всмпо-авсм|всмпо|авсм|vsmpo|avsm|vsmpo-avsm|vsmo)\s",
    "AFLT": r"\s(:?аэрофлот|aflt|aeroflot)\s",
    "AKRN": r"\s(:?акрон|akrn|akron)\s",
    "SELG": r"\s(:?селигдар|selg|seligdar)\s",
    "NKNC": r"\s(:?нкнх|нижнекамскнефтехим|nknc)\s",
    # Six
    "BSPB": r"\s(:?бсп|банк санкт-петербург|банк спб|bspb|bsp)\s",
    "LENT": r"\s(:?лента|lenta|lent)\s",
    "GEMC": r"\s(:?gemc|united medical)\s",
    "KZOS": r"\s(:?казаньоргсинтез|оргсинт|kzos|kazanorgsintez)\s",
    "MGTS": r"\s(:?мгтс|mgts|московская городская телефонная сеть)\s",
    "MSNG": r"\s(:?мосэнерго|\+мосэнерго|mosenergo|\+mosenergo|msng)\s",
    "SMLT": r"\s(:?гк самолет|smlt|gk samolet)\s",
    "NMTP": r"\s(:?нмтп|nmtp|новороссийский морской торговый порт)\s",
    "UPRO": r"\s(:?юнипро|upro|unipro)\s",
    "FESH": r"\s(:?двмп|fesh|дальневосточное морское пароходство|dvmp)\s",
    # Seven
    "BELU": r"\s(:?новабев|belu|novabev)\s",
    "QIWI": r"\s(:?qiwi|киви|iqiwi|айкиви)\s",
    "MDMG": r"\s(:?mdmg|md medical)\s",
    "POSI": r"\s(:?iпозитив|группа позитив|ipositiv|positiv|posi)\s",
    "RASP": r"\s(:?распадская|raspadskaya|rasp)\s",
    "LSRG": r"\s(:?лср|группа лср|lsr|lsrg)\s",
    "LSNG": r"\s(:?россети ленэнерго|ленэнерго|lenenergo|lsng)\s",
    "SGZH": r"\s(:?сегежа|segezha|sgzh)\s",
    # Eight
    "RSTI": r"\s(:?rsti|российские сети|россети|rosseti)\s",
    "OGKB": r"\s(:?огк-2|ogk-2|ogkb)\s",
    "AQUA": r"\s(:?инарктика|aqua|inarctica)\s",
    "ETLN": r"\s(:?etalon|etln|группа эталон|эталон)\s",
    "RENI": r"\s(:?ренессанс страхование|группа ренессанс|reni)\s",
    "NKHP": r"\s(:?нкхп|nkhp|новороссийский комбинат хлебопродуктов)\s",
    "MRKP": r"\s(:?рсетицп|россети центр и приволжье|mrkp)\s",
    "MRKC": r"\s(:?россцентр|россети центр|mrkc)\s",
    "MVID": r"\s(:?м\.видео|мвидео|mvideo|m\.video|mvid)\s",
    "ELFV": r"\s(:?эл5-энерго|эл5энер|эл5|el5ener|el5-energo|el5|elfv)\s",
    # Nine
    "TGKA": r"\s(:?тгк-1|tgka|tgk-1)\s",
    "RNFT": r"\s(:?русснфт|русснефть|rnft|russneft|russnft)\s",
    "APTK": r"\s(:?аптеки36и6|аптечная сеть 36,6|aptk)\s",
    "MSRS": r"\s(:?рсетимр|россети московский регион|msrs|rsetimr)\s",
    "SFIN": r"\s(:?эсэфай|sfi|сафмар|sfin)\s",
    "MRKU": r"\s(:?россети урал|россети ур|rosseti ural|rosseti ur|mrku)\s",
    "SVAV": r"\s(:?соллерс|sollers|svav)\s",
    "CIAN": r"\s(:?циан|cian)\s",
    "TGKB": r"\s(:?тгк-2|tgkb|tgk-2)\s",
    # Ten
    "DVEC": r"\s(:?дэк|дальневосточная энергетическая компания|dec|dvec)\s",
    "RKKE": r"\s(:?энергияркк|ркк энергия|rkk energia|rkk energiya|rkke)\s",
    "MRKZ": r"\s(:?рсетисз|россети северо-запад|mrkz)\s",
    "WUSH": r"\s(:?iвушхолднг|вуш|wush|whoosh)\s",
    "TTLK": r"\s(:?таттел|таттелеком|ttlk|tattelecom|tattel)\s",
    "MRKV": r"\s(:?рсетвол|россети волга|mrkv)\s",
    "ABIO": r"\s(:?iартген|артген|abio|artgen)\s",
    "CHMK": r"\s(:?чмк|челябинский металлургический комбинат|chmk)\s",
    "OKEY": r"\s(:?okey|o'key|окей|о'кей)\s",
    # More
    "VKCO": r"\s(:?вк|vk|вконтакте|vkontakte|в контакте|v kontakte|vkco)\s",
}

industries = {
    # Нефть и газ
    "MOEXOG": ["BANE", "GAZP", "LKOH", "NVTK", "RNFT", "ROSN", "SNGS", "TATN", "TRNF"],
    # Электроэнергетики
    "MOEXEU": [
        "IRAO",
        "HYDR",
        "FEES",
        "MSNG",
        "UPRO",
        "LSNG",
        "RSTI",
        "OGKB",
        "MRKP",
        "MRKC",
        "ELFV",
        "TGKA",
        "MSRS",
        "MRKU",
        "TGKB",
        "DVEC",
        "MRKZ",
        "MRKV",
    ],
    # Телекоммуникации
    "MOEXTL": ["MTSS", "RTKM", "MGTS", "TTLK"],
    # Металлы и добыча
    "MOEXMM": [
        "GMKN",
        "PLZL",
        "CHMF",
        "NLMK",
        "POLY",
        "ALRS",
        "MAGN",
        "RUAL",
        "ENPG",
        "MTLR",
        "VSMO",
        "SELG",
        "RASP",
        "SGZH",
        "CHMK",
    ],
    # Финансы
    "MOEXFN": ["SBER", "TCSG", "VTBR", "CBOM", "BSPB", "QIWI", "RENI", "SFIN", "AFKS"],
    # Потребительский сектор
    "MOEXCN": [
        "MGNT",
        "FIVE",
        "FIXP",
        "AGRO",
        "GEMC",
        "LENT",
        "BELU",
        "MDMG",
        "AQUA",
        "MVID",
        "APTK",
        "SVAV",
        "WUSH",
        "ABIO",
        "OKEY",
    ],
    # Химия и нефтехимия
    "MOEXCH": ["PHOR", "KAZT", "AKRN", "NKNC", "KZOS"],
    # Транспорт
    "MOEXTN": ["GLTR", "FLOT", "AFLT", "NMTP", "FESH", "NKHP", "RKKE"],
    # Информационные технологии
    "MOEXIT": ["CIAN", "HHRU", "OZON", "POSI", "VKCO", "YNDX"],
    # Строительные компании
    "MOEXRE": ["ETLN", "LSRG", "PIKK", "SMLT"],
}

politicians = {
    # One
    "путин": r"путин",
    "мишустин": r"мишустин",
    "вайно": r"вайно",
    "медведев": r"медведев",
    "собянин": r"собянин",
    "кириенко": r"кириенко",
    "лавров": r"лавров",
    "патрушев": r"патрушев",
    "шойгу": r"шойгу",
    "миллер": r"миллер",
    # Two
    "сечин": r"сечин",
    "силуанов": r"силуанов",
    "громов": r"громов",
    "набиуллина": r"набиуллина",
    "турчак": r"турчак",
    "бортников": r"бортников",
    "володин": r"володин",
    "песков": r"песков",
    "бастрыкин": r"бастрыкин",
    "белоусов": r"белоусов",
    # Three
    "нарышкин": r"нарышкин",
    "чемезов": r"чемезов",
    "матвиенко": r"матвиенко",
    "греф": r"греф",
    "золотов": r"золотов",
    "колокольцев": r"колокольцев",
    "тимченко": r"тимченко",
    "ковальчук": r"ковальчук",
    "патриарх": r"патриарх",
    "хуснуллин": r"хуснуллин",
    # Four
    "борисов": r"борисов",
    "голикова": r"голикова",
    "новак": r"новак",
    "герасимов": r"герасимов",
    "костин": r"костин",
    "козак": r"козак",
    "патрушев": r"патрушев",
    "чернышенко": r"чернышенко",
    "ярин": r"ярин",
    "мантуров": r"мантуров",
    # Five
    "трутнев": r"трутнев",
    "григоренко": r"григоренко",
    "левитин": r"левитин",
    "краснов": r"краснов",
    "усманов": r"усманов",
    "васильев": r"васильев",
    "оверчук": r"оверчук",
    "ротенберг": r"ротенберг",
    "харичев": r"харичев",
    "чиханчин": r"чиханчин",
}

federal_instances = {
    "ЦБ": r"\s(?:цб|центральный банк|центробанк)\s",
    "МинФин": r"\s(?:министерство финансов|минфин)\s",
    "ФНС": (
        r"\s(?:федеральная налоговая служба|фнс|налоговая служба|"
        r"налоговый департамент|налоговое ведомство|налоговое управление)\s"
    ),
    "ФСФМ": (
        r"\s(?:федеральная служба финансового мониторинга|финмониторинг|"
        r"федеральная служба по финансовым операциям|фсфм)\s"
    ),
    "ПФР": r"\s(?:пенсионный фонд|пфр|фонд пенсионного обеспечения|фонд соцзащиты)\s",
    "ФНБ": r"\s(?:фонд национального благосостояния|фнб|фонд стабилизации|фонд)\s",
    "ФК": r"\s(?:казначейство|фк|финансовая служба)\s",
    "ММВБ": (
        r"\s(?:ммвб|московская биржа|moex|rts|российская торговая система"
        r"|биржевой индекс)\s"
    ),
}

additional_stopwords = [
    "которых",
    "которые",
    "твой",
    "которой",
    "которого",
    "сих",
    "ком",
    "свой",
    "твоя",
    "этими",
    "слишком",
    "нами",
    "всему",
    "будь",
    "саму",
    "чаще",
    "ваше",
    "сами",
    "наш",
    "затем",
    "самих",
    "наши",
    "ту",
    "каждое",
    "мочь",
    "весь",
    "этим",
    "наша",
    "своих",
    "оба",
    "который",
    "зато",
    "те",
    "этих",
    "вся",
    "ваш",
    "такая",
    "теми",
    "ею",
    "которая",
    "нередко",
    "каждая",
    "также",
    "чему",
    "собой",
    "самими",
    "нем",
    "вами",
    "ими",
    "откуда",
    "такие",
    "тому",
    "та",
    "очень",
    "сама",
    "нему",
    "алло",
    "оно",
    "этому",
    "кому",
    "тобой",
    "таки",
    "твоё",
    "каждые",
    "твои",
    "нею",
    "самим",
    "ваши",
    "ваша",
    "кем",
    "мои",
    "однако",
    "сразу",
    "свое",
    "ними",
    "всё",
    "неё",
    "тех",
    "хотя",
    "всем",
    "тобою",
    "тебе",
    "одной",
    "другие",
    "само",
    "эта",
    "самой",
    "моё",
    "своей",
    "такое",
    "всею",
    "будут",
    "своего",
    "кого",
    "свои",
    "мог",
    "нам",
    "особенно",
    "её",
    "самому",
    "наше",
    "кроме",
    "вообще",
    "вон",
    "мною",
    "никто",
    "это",
]


months = {
    "января": "1",
    "февраля": "2",
    "марта": "3",
    "апреля": "4",
    "мая": "5",
    "июня": "6",
    "июля": "7",
    "августа": "8",
    "сентября": "9",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


def month_convert(date: str) -> str:
    """
    Convert date's month name to month number.

    :param date: date of the news
    :type date: str

    :rtype: str
    :return date: date with month name converted month number
    """
    for word, initial in months.items():
        date = date.replace(word.lower(), initial)
    return date


def date_changer(date: str, convert_month: bool, pattern: str) -> datetime:
    """
    Convert date to certain format and transform to datetime type.

    :param date: date of the news
    :type date: str
    :param convert_month: is month conversion required
    :type convert_month: bool
    :param pattern: final format of the date
    :type pattern: str

    :rtype: datetime
    :return datetime_object: date in certain format and in datetime type
    """
    if convert_month:
        date = month_convert(date)

    datetime_object = datetime.strptime(date, pattern)
    return datetime_object


def date_ria_extract(df: pd.DataFrame) -> list[str]:
    """
    Extract dates from the Ria news.

    :param df: dataset with date column
    :type df: pd.DataFrame

    :rtype: list[str]
    :return dates_init: dates of Ria
    """
    pattern = (
        r"^([0-1]?[0-9]|2?[0-3]):([0-5]\d)\s([1-9]|([012][0-9])"
        r"|(3[01]))[.]([0]{0,1}[1-9]|1[012])[.]\d\d\d\d"
    )
    dates_init = []

    for i in df.date:
        result = re.match(pattern, i)
        dates_init.append(result[0])

    return dates_init


def third_thursday(year: int, month: int) -> date:
    """
    Return date for monthly option expiration given year and month.

    :param year: year of the date
    :type year: int
    :param month: month of the date
    :type month: int

    :rtype: date
    :return third: date for monthly option expiration
    """
    # The 15th is the lowest third day in the month
    third = date(year, month, 15)
    # What day of the week is the 15th?
    w = third.weekday()
    # Thursday is weekday 3
    if w != 3:
        # Replace just the day (of month)
        third = third.replace(day=(15 + (3 - w) % 7))
    return third
