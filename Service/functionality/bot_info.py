from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from utils.text_messages import ABOUT_SERVICE, DISCLAIMER

router = Router()


@router.callback_query(F.data == "about_service")
async def msg_about_service(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(ABOUT_SERVICE, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "disclaimer")
async def msg_disclaimer(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN_V2)
