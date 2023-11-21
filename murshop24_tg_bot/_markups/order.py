from collections.abc import Iterable

import murshop24_models as models  # type: ignore
import pytz  # type: ignore
from aiogram import types
from aiogram.utils import keyboard
from murshop24_models import enums as model_enums  # type: ignore

from murshop24_tg_bot import _callback_data, _consts

_months = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def orders(orders: Iterable[models.Order]) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for order in orders:
        created_at = order.created_at.replace(tzinfo=pytz.utc).astimezone(
            pytz.timezone(_consts.PYTZ_TIMEZONE)
        )
        match order.status:
            case model_enums.OrderStatus.CANCELED:
                status = "🚫"
            case _:
                status = "⏳"
        text = (
            f"{status} {created_at.day} {_months[created_at.month]}, "
            f"{created_at.strftime('%H:%M')} · {order.price}тг"
        )
        builder.button(text=text, callback_data=_callback_data.Order(id=order.id))
    builder.button(text="‹ Назад", callback_data=_consts.CallbackData.START)
    builder.adjust(1)
    return builder.as_markup()


def order(order: models.Order, can_confirm: bool = True, can_cancel: bool = True) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    if can_confirm:
        builder.button(
            text="Оплатил",
            callback_data=_callback_data.Order(id=order.id, confirm=True),
        )
    if can_cancel:
        builder.button(
            text="Отменить",
            callback_data=_callback_data.Order(id=order.id, cancel=True),
        )
    builder.button(text="‹ Назад", callback_data=_consts.CallbackData.ORDERS)
    builder.adjust(1)
    return builder.as_markup()
