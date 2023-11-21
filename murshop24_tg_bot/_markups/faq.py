from aiogram import types
from aiogram.utils import keyboard

from murshop24_tg_bot import _consts


def faq() -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(text="‹ Назад", callback_data=_consts.CallbackData.START)
    return builder.as_markup()
