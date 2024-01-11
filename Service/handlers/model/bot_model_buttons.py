from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def model_btns() -> InlineKeyboardMarkup:
    """
    Inline buttons for the models prediction.

    :rtype: ReplyKeyboardMarkup
    :return kb: keyboard markup
    """
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="More information about the model",
            callback_data="model_info",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="Insert link of the news to make prediction",
            callback_data="insert_link",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="Insert text of the news to make prediction",
            callback_data="insert_text",
        )
    )

    return kb.as_markup()
