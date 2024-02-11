from aiogram import F, Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from utils.database import read_feedback_from_db

router = Router()


@router.callback_query(F.data == "show_feedback")
async def show_feedback(callback: CallbackQuery) -> None:
    """
    Sends reviews as a message.

    :param callback: average of scores, all reviews
    :type callback: CallbackQuery
    """
    if callback.message:
        text = await read_feedback_from_db()
        await callback.answer(cache_time=1)
        await callback.message.answer(text, reply_markup=ReplyKeyboardRemove())
