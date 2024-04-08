from aiogram import Router

from . import (
    bot_display_feedback,
    bot_display_ticker,
    bot_get_feedback,
    bot_graph,
    bot_info,
    bot_start,
)
from .model import bot_model_main


def get_routers() -> list[Router]:
    return [
        bot_start.router,
        bot_info.router,
        bot_get_feedback.router,
        bot_display_feedback.router,
        bot_display_ticker.router,
        bot_graph.router,
        bot_model_main.router,
    ]
