from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

router = Router()

ABOUT_SERVICE = f"""s
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

DISCLAIMER = f"""
Service is still in the development, that is why:
 \- Not all features are implemented yet
 \- Some bugs can arise
 \- Models are not finished yet and will be improved in the future
 
If you faced any bugs, have any recommendations or just want to leave your feedback, please, leave you rating and the comment in the correspondning section\. 

Our team will really appreciate this\! <3
"""


@router.callback_query(F.data == "about_service")
async def msg_about_service(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(ABOUT_SERVICE, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "disclaimer")
async def msg_disclaimer(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN_V2)
