from collections.abc import Iterable

from aiogram import types
from aiogram.utils import keyboard
from aiogram.filters import callback_data
import murshop24_models as models  # type: ignore

from murshop24_tg_bot import _callback_data, _consts


def select_city(cities: Iterable[models.City]) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for city in cities:
        builder.button(text=city.name, callback_data=_callback_data.City(id=city.id))
    builder.button(text="‹ Назад", callback_data=_consts.CallbackData.START)
    builder.adjust(1)
    return builder.as_markup()


def select_product(products: Iterable[models.Product]) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=product.name, callback_data=_callback_data.Product(id=product.id)
        )
    builder.button(text="‹ Назад", callback_data=_consts.CallbackData.CATALOG)
    builder.adjust(1)
    return builder.as_markup()


def select_district(
    districts: Iterable[models.District],
    back_callback_data: callback_data.CallbackData | str,
) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for district in districts:
        builder.button(
            text=district.name, callback_data=_callback_data.District(id=district.id)
        )
    builder.button(text="‹ Назад", callback_data=back_callback_data)
    builder.adjust(1)
    return builder.as_markup()


def select_product_unit(
    district_product_units: Iterable[models.DistrictProductUnit],
    back_callback_data: callback_data.CallbackData | str,
) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    for district_product_unit in district_product_units:
        product_unit = district_product_unit.product_unit
        product_unit_str = models.ProductUnit.create_str(product_unit)
        text = f"{product_unit_str} · {district_product_unit.price}тг"
        builder.button(
            text=text,
            callback_data=_callback_data.ProductUnit(id=product_unit.id),
        )
    builder.button(text="‹ Назад", callback_data=back_callback_data)
    builder.adjust(1)
    return builder.as_markup()


def select_payment_method(
    back_callback_data: callback_data.CallbackData | str,
) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(
        text="Банковский перевод",
        callback_data=_callback_data.PaymentMethod(
            name=_callback_data.PaymentMethodName.BANK
        ),
    )
    builder.button(
        text="QIWI Кошелек",
        callback_data=_callback_data.PaymentMethod(
            name=_callback_data.PaymentMethodName.QIWI_WALLET
        ),
    )
    builder.button(text="‹ Назад", callback_data=back_callback_data)
    builder.adjust(1)
    return builder.as_markup()


def payment_method_bank(
    back_callback_data: callback_data.CallbackData | str,
) -> types.InlineKeyboardMarkup:
    builder = keyboard.InlineKeyboardBuilder()
    builder.button(
        text="Создать заказ", callback_data=_consts.CallbackData.CREATE_ORDER
    )
    builder.button(text="‹ Назад", callback_data=back_callback_data)
    builder.adjust(1)
    return builder.as_markup()
