import aiogram
import murshop24_models as models  # type: ignore
from aiogram import types
from aiogram.fsm import context as fsm_context
from murshop24_models import enums as model_enums  # type: ignore
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _callback_data, _consts
from murshop24_tg_bot._db import catalog as catalog_db
from murshop24_tg_bot._db import order as db
from murshop24_tg_bot._markups import order as markups

router = aiogram.Router(name=__name__)


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.ORDERS, aiogram.F.message.is_not(None)
)
async def cq_orders(
    callback_query: types.CallbackQuery,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    async with async_session() as session:
        orders = await db.select_orders(session, callback_query.from_user.id)
    if not orders:
        text = "Здесь будут отображаться ваши заказы."
    else:
        text = "Ваши заказы:"
    markup = markups.orders(orders)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


async def show_order(
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession], id: int
) -> tuple[str, types.InlineKeyboardMarkup]:
    async with async_session() as session:
        order = await db.select_order(session, id)
        city = await db.select_city(session, order.district_id)
        district = order.district
        product = await db.select_product(session, order.product_unit_id)
        product_unit = order.product_unit
        district_product_unit = await db.select_district_product_unit(
            session, district.id, product_unit.id
        )
        bank_account = order.bank_account
        bank: models.Bank | None = None
        if bank_account is not None:
            bank = await bank_account.awaitable_attrs.bank
        qiwi_wallet_account = order.qiwi_wallet_account
    match order.status:
        case model_enums.OrderStatus.PAYMENT_WAITING:
            order_status = "Ожидается оплата"
        case model_enums.OrderStatus.PAYMENT_CHECKING:
            order_status = "Платеж проверяется"
        case model_enums.OrderStatus.PROCESSING:
            order_status = "В обработке"
        case model_enums.OrderStatus.COMPLETED:
            order_status = "Завершен"
        case model_enums.OrderStatus.CANCELED:
            order_status = "Отменен"
    if order.bank_account_id is not None and bank is not None:
        payment_method = "Банковский перевод"
        if bank_account.phone_number is not None:
            payment = (
                "<strong>Реквизиты для оплаты:</strong>\n"
                f"Банк: {bank.name}\n"
                f"Номер карты: {bank_account.card_number}\n"
                f"Номер телефона: {bank_account.phone_number}"
            )
        else:
            payment = (
                "<strong>Реквизиты для оплаты:</strong>\n"
                f"Банк: {bank.name}\n"
                f"Номер карты: {bank_account.card_number}\n"
            )
    elif order.qiwi_wallet_account_id is not None:
        payment_method = "QIWI Кошелек"
        if (
            qiwi_wallet_account.phone_number is not None
            and qiwi_wallet_account.nickname is not None
        ):
            payment = (
                "<strong>Реквизиты для оплаты:</strong>\n"
                f"Номер телефона: {qiwi_wallet_account.phone_number}\n"
                f"Никнейм: {qiwi_wallet_account.nickname}"
            )
        elif (
            qiwi_wallet_account.phone_number is not None
            and qiwi_wallet_account.nickname is None
        ):
            payment = (
                "<strong>Реквизиты для оплаты:</strong>\n"
                f"Номер телефона: {qiwi_wallet_account.phone_number}"
            )
        else:
            payment = (
                "<strong>Реквизиты для оплаты:</strong>\n"
                f"Никнейм: {qiwi_wallet_account.nickname}"
            )
    match order.status:
        case model_enums.OrderStatus.PAYMENT_WAITING | model_enums.OrderStatus.PAYMENT_CHECKING:
            text = (
                f"<strong>📄 Заказ #{order.id}</strong>\n\n"
                f"<strong>Город:</strong> {city.name}\n"
                f"<strong>Район:</strong> {district.name}\n"
                f"<strong>Товар:</strong> "
                f"{product.name} {models.ProductUnit.create_str(product_unit)}\n"
                f"<strong>Цена:</strong> {district_product_unit.price}тг\n"
                f"<strong>Способ оплаты:</strong> {payment_method}\n"
                f"<strong>Статус:</strong> {order_status}\n\n"
                f"{payment}"
            )
        case _:
            text = (
                f"<strong>📄 Заказ #{order.id}</strong>\n\n"
                f"<strong>Город:</strong> {city.name}\n"
                f"<strong>Район:</strong> {district.name}\n"
                f"<strong>Товар:</strong> "
                f"{product.name} {models.ProductUnit.create_str(product_unit)}\n"
                f"<strong>Цена:</strong> {district_product_unit.price}тг\n"
                f"<strong>Способ оплаты:</strong> {payment_method}\n"
                f"<strong>Статус:</strong> {order_status}"
            )
    can_confirm_or_cancel = (
        True if order.status == model_enums.OrderStatus.PAYMENT_WAITING else False
    )
    markup = markups.order(order, can_confirm=can_confirm_or_cancel, can_cancel=can_confirm_or_cancel)
    return text, markup


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.CREATE_ORDER, aiogram.F.message.is_not(None)
)
async def cq_create_order(
    callback_query: types.CallbackQuery,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    data = await state.get_data()
    district_id: int = data["district_id"]
    product_unit_id: int = data["product_unit_id"]
    payment_method_name: str = data["payment_method_name"]
    async with async_session() as session:
        district = await db.select_district(session, district_id)
        product_unit = await db.select_product_unit(session, product_unit_id)
        bank_account: models.BankAccount | None = None
        qiwi_wallet_account: models.QiwiWalletAccount | None = None
        match _callback_data.PaymentMethodName(payment_method_name):
            case _callback_data.PaymentMethodName.BANK:
                bank_account = await catalog_db.select_bank_account(session)
            case _callback_data.PaymentMethodName.QIWI_WALLET:
                qiwi_wallet_account = await catalog_db.select_qiwi_wallet_account(
                    session
                )
        tg_customer = await db.select_tg_customer(session, callback_query.from_user.id)
        order = await db.insert_order(
            session,
            tg_customer,
            district,
            product_unit,
            bank_account,
            qiwi_wallet_account,
        )
        await session.commit()
    text, markup = await show_order(async_session, order.id)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(
    _callback_data.Order.filter(aiogram.F.cancel),
    aiogram.F.message.is_not(None),
)
async def cq_cancel_order(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.Order,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    async with async_session() as session:
        await db.cancel_order(session, callback_data.id)
        await session.commit()
    text, markup = await show_order(async_session, callback_data.id)
    await callback_query.answer(text="Заказ успешно отменен.")
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(
    _callback_data.Order.filter(aiogram.F.confirm),
    aiogram.F.message.is_not(None),
)
async def cq_confirm_order(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.Order,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    async with async_session() as session:
        await db.confirm_order(session, callback_data.id)
        await session.commit()
    text, markup = await show_order(async_session, callback_data.id)
    await callback_query.answer(text="Вы подтвердили оплату.")
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(_callback_data.Order.filter(), aiogram.F.message.is_not(None))
async def cq_order(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.Order,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    text, markup = await show_order(async_session, callback_data.id)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
