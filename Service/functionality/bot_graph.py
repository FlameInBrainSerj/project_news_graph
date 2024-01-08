from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hide_link

router = Router()

CAT_LINK = "https://cataas.com/cat"
CAT_MESSAGE = f"""{hide_link(CAT_LINK)} MEOW 🐱"""
GRAPH_MESSAGE = f"""
Sorry, my creators haven't completed me yet 🫣, but instead I can send you image of a pretty cat 🤗
"""


@router.callback_query(F.data == "display_graph")
async def msg_display_graph(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(GRAPH_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)
    await callback.message.answer(CAT_MESSAGE, parse_mode=ParseMode.HTML)
