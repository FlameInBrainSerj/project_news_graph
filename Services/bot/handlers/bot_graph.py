from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hide_link
from utils.text_messages import MSG_DISPLAY_GRAPH

router = Router()

CAT_LINK = "https://cataas.com/cat"


@router.callback_query(F.data == "display_graph")
async def msg_display_graph(callback: CallbackQuery) -> None:
    """
    Display message about the graph.

    :param callback: text of the message about the graph
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            MSG_DISPLAY_GRAPH.format(link=hide_link(CAT_LINK)),
            parse_mode=ParseMode.HTML,
        )
