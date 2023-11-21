from aiogram import types
from aiogram.utils import keyboard
import murshop24_models as models  # type: ignore

from murshop24_tg_bot import _consts


def start(
    tg_operator: models.TgOperator,
    tg_reviews_channel: models.TgReviewsChannel | None = None,
) -> types.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()
    keyboard_builder.button(text="Каталог", callback_data=_consts.CallbackData.CATALOG)
    keyboard_builder.button(
        text="Мои заказы", callback_data=_consts.CallbackData.ORDERS
    )
    keyboard_builder.button(text="Правила", callback_data=_consts.CallbackData.RULES)
    keyboard_builder.button(text="FAQ", callback_data=_consts.CallbackData.FAQ)
    keyboard_builder.button(
        text="Оператор", url=f"https://t.me/{tg_operator.tg_username}"
    )
    if tg_reviews_channel is not None:
        keyboard_builder.button(text="Отзывы", url=tg_reviews_channel.invite_link)
    keyboard_builder.adjust(1, 1, 2, 1 if tg_reviews_channel is None else 2)
    return keyboard_builder.as_markup()
