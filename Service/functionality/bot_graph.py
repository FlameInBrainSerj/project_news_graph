from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hide_link

from utils.text_messages import GRAPH_MSG

router = Router()

CAT_LINK = "https://cataas.com/cat"


@router.callback_query(F.data == "display_graph")
async def msg_display_graph(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        GRAPH_MSG.format(link=hide_link(CAT_LINK)),
        parse_mode=ParseMode.HTML,
    )
