from aiogram import types
from aiogram.utils import keyboard

from murshop24_tg_bot import _consts


def tg_bot_error() -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(text="‹ На главную", callback_data=_consts.CallbackData.START)
    return builder.as_markup()
