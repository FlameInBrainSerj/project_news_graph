from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from utils.text_messages import ABOUT_SERVICE, DISCLAIMER

router = Router()


@router.callback_query(F.data == "about_service")
async def msg_about_service(callback: CallbackQuery) -> None:
    """
    Display detailed information about the service.

    :param callback: text of the information about the service
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(ABOUT_SERVICE, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "disclaimer")
async def msg_disclaimer(callback: CallbackQuery) -> None:
    """
    Display disclaimer.

    :param callback: text of the disclaimer
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN_V2)
