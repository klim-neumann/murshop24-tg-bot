import enum

from aiogram.filters import callback_data


class PaymentMethodName(enum.StrEnum):
    BANK = enum.auto()
    QIWI_WALLET = enum.auto()


class City(callback_data.CallbackData, prefix="city"):
    id: int


class Product(callback_data.CallbackData, prefix="product"):
    id: int


class District(callback_data.CallbackData, prefix="district"):
    id: int


class ProductUnit(callback_data.CallbackData, prefix="product_unit"):
    id: int


class PaymentMethod(callback_data.CallbackData, prefix="payment_method"):
    name: PaymentMethodName


class Order(callback_data.CallbackData, prefix="order"):
    id: int
    confirm: bool = False
    cancel: bool = False
