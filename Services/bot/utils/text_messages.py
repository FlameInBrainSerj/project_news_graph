ABOUT_SERVICE = (
    "This service was created as a part of the project: "
    "'Building the news graph and services connected to it'\n\n"
    "This project is dedicated to analysis of news using NLP and graph methods\n\n"
    "What features already realised \(for now\):\n"
    "    \- Make prediction, how certain news can influence financial instrument\n"
    "    \- Display information about the certain ticker\n"
    "    \- Add graph of connections between financial entities\n\n"
    "Creators: @FlameInBrain, @maxodum\n\n"
    "Detailed description of the project and steps completed can be found"
    "can be found in the GitHub repository: "
    "[github repo](https://github.com/FlameInBrainSerj/project_news_graph)"
)

DISCLAIMER = (
    "Service\-bot is still in the development, that is why:\n"
    " \- Not all features are implemented yet\n"
    " \- Some bugs can arise\n"
    " \- Models are not finished yet and will "
    "be improved in the future\n\n"
    "If you faced any bugs, have any recommendations or just want to "
    "leave your feedback, please, leave you rating and the comment "
    "in the correspondning section\.\n\n"
    "Our team will really appreciate this\! <3"
)

MODEL_INFO = (
    "This model was created with NLP methods and aimed to make "
    "predictions of news' influence on financial instruments in "
    "accordance with certain levels\n\n"
    "_*Levels:*_\n"
    "\- *Global*: MOEX index, RVI index, RUBUSD course\n"
    "\- *Indsutry*: industrial indicies \(i\.e\. MOEXOG, MOEXEU, "
    "MOEXTL, etc\.\)\n"
    "\- *Company*: companies' share price according to ticker "
    "\(i\.e\. VKCO, SBER, YNDX, etc\.\)\n\n"
    "_*Model's output:*_ label of influence on financial instrument "
    "\(Negative, Neutral, Positive\)\n\n"
    "_*Model's constraints:*_\n"
    "\- Model was trained on Russian financial news and is only "
    "applicable to these kind of news\n"
    "\- Model is sensetive only to companies from top\-100 of Russian "
    "market basing on MOEX index\n"
    "\- It is highly recommended to pass news with no more than 1\-2 "
    "companies, otherwise results could be inadequate"
)

INSERT_LINK_MSG = """
Please, send the link to the news in the chat and wait for approximately 15 seconds

*Currently only these news portals are available: {websites}

So, be sure to send link from one of these websites
"""

INSERT_TEXT_MSG = """
Please, send the text of the news in the chat
"""

PREDICTION_LEVEL_1 = (
    "No companies from top\-100 of Russian financial market "
    "were found in the text of the news, that is why only effect "
    "on global financial instruments is present\.\n\n"
    "The effect of this news on financial instruments is the following:\n"
    "        \-\-\- *MOEX index:* __{moex_index_label}__\n"
    "        \-\-\- *RVI index:* __{rvi_index_label}__\n"
    "        \-\-\- *RUBUSD course:* __{rubusd_index_label}__"
)

PREDICTION_LEVEL_3 = """
The effect of this news on financial instruments is the following:
\(including the mentioned company and associated industry\)

        \-\-\- *Company's share price:* __{comp_share_price_label}__
        \-\-\- *Industrial index:* __{ind_index_label}__
        \-\-\- *MOEX index:* __{moex_index_label}__
        \-\-\- *RVI index:* __{rvi_index_label}__
        \-\-\- *RUBUSD course:* __{rubusd_index_label}__
"""

TICKER_DESCRIPTION = """
Open — the opening price of the previous trading hour
Close — the closing price of the previous trading hour
Highest — the highest price for the previous trading hour
Lowest — the lowest price for the previous trading hour
Value — combined value of all operations in the previous trading hour
Volume — amount of trades in the previous trading hour
Begin — the start of the previous trading hour
End — the end of the previous trading hour\n\n"""

MSG_DISPLAY_GRAPH = (
    "Sorry, my creators haven't completed me yet 🫣, but "
    "instead I can send you an image of a pretty cat 🤗\n\n"
    "{link}MEOW 🐱"
)


MSG_DISPLAY_TICKER = (
    "Please select the ticker of the company represented in the "
    "broad market index of the Moscow Stock Exchange"
)

MSG_CHOOSE_TICKER = (
    "Wrong ticker!\n"
    "Please select the ticker of the company represented "
    "in the broad market index of the Moscow Stock Exchange"
)

ERROR_MSG_PAGE_NOT_LOADED = (
    "Sorry, the page was not parsed :(, please, try insert "
    "the same link again or try insert the text of the news "
    "using corresponding buttons"
)
