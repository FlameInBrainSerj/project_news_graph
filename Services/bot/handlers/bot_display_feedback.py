from aiogram import F, Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import read_feedback_from_db

router = Router()


@router.callback_query(F.data == "show_feedback")
async def show_feedback(callback: CallbackQuery, session: AsyncSession) -> None:
    """
    Sends reviews as a message.

    :param callback: average of scores, all reviews
    :type callback: CallbackQuery
    :param session: database session
    :type session: AsyncSession
    """
    if callback.message:
        text = await read_feedback_from_db(session)
        await callback.answer(cache_time=1)
        await callback.message.answer(text, reply_markup=ReplyKeyboardRemove())
