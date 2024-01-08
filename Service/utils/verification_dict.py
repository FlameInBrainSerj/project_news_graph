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
