from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def model_btns() -> ReplyKeyboardMarkup:
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
