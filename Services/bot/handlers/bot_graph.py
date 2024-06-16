import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from utils.text_messages import MSG_DISPLAY_GRAPH

logger = logging.getLogger(__name__)
router = Router()

streamlit_link = "https://project-news-analysis-eda.streamlit.app/"


@router.callback_query(F.data == "display_graph")
async def msg_display_graph(callback: CallbackQuery) -> None:
    """
    Display message about the graph.

    :param callback: text of the message about the graph
    :type callback: CallbackQuery
    """
    logger.info("The 'display_graph' was triggered")

    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            MSG_DISPLAY_GRAPH.format(link=streamlit_link),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
