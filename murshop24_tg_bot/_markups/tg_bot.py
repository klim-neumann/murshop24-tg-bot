from collections.abc import Iterable

import murshop24_models as models  # type: ignore
from aiogram import types
from aiogram.utils import keyboard


def tg_bot_not_exists(
    tg_operators: Iterable[models.TgOperator],
    use_tg_username: bool,
) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for tg_operator in tg_operators:
        url = f"https://t.me/{tg_operator.tg_username}"
        if use_tg_username:
            text = tg_operator.tg_username
        else:
            text = "Оператор"
        builder.button(text=text, url=url)
    builder.adjust(1)
    return builder.as_markup()
