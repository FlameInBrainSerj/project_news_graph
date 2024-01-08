ABOUT_SERVICE = """
This service was created as a part of the project: 'Building the news graph and services connected to it'   

This project is dedicated to analysis of news using NLP and GNN methods   

What features already realised \(for now\):   
    \- Make prediction, how certain news can influence financial instrument
    \- Display information about the certain ticket

What is planned to be done:   
    \- Add graph of connections between financial entities
    \- Apply GNN methods

Creators: @FlameInBrain, @maxodum   

Detailed description of the project and steps 
completed can be found in the GitHub repository: [github repo](https://github.com/FlameInBrainSerj/project_news_graph)
"""

DISCLAIMER = """
Service is still in the development, that is why:
 \- Not all features are implemented yet
 \- Some bugs can arise
 \- Models are not finished yet and will be improved in the future

If you faced any bugs, have any recommendations or just want to leave your feedback, please, leave you rating and the comment in the correspondning section\. 

Our team will really appreciate this\! <3
"""

MODEL_INFO = """
This model was created with NLP methods and aimed to make predictions of news' influence on financial instruments in accordance with certain levels

_*Levels:*_
\- *Global*: MOEX index, RVI index, RUBUSD course
\- *Indsutry*: industrial indicies \(i\.e\. MOEXOG, MOEXEU, MOEXTL, etc\.\)
\- *Company*: companiпринes' share price according to ticket \(i\.e\. VKCO, SBER, YNDX, etc\.\)

_*Model's output:*_ label of influence on financial instrument \(Negative, Neytral, Positive\)

_*Model's constraints:*_
\- Model was trained on Russian financial news and is only applicable to these kind of news
\- Model is sensetive only to companies from top\-100 of Russian market basing on MOEX index
\- It is highly recommended to pass news with no more than 1\-2 companies, otherwise results could be inadequate
"""

INSERT_LINK_MSG = """
Please, send the link to the news in the chat

*Currently only these news portals are available: {websites}

So, be sure to send link from one of these websites 
"""

INSERT_TEXT_MSG = """
Please, send the text to the news in the chat with '/text' before the news body
"""

GRAPH_MSG = """
Sorry, my creators haven't completed me yet 🫣, but instead I can send you an image of a pretty cat 🤗

{link}MEOW 🐱
"""
