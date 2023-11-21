import aiogram
import murshop24_models as models  # type: ignore
from aiogram import types
from aiogram.fsm import context as fsm_context
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _callback_data, _consts
from murshop24_tg_bot._markups import catalog as markups
from murshop24_tg_bot._db import catalog as db

router = aiogram.Router(name=__name__)


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.CATALOG, aiogram.F.message.is_not(None)
)
async def cq_select_city(
    callback_query: types.CallbackQuery,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    async with async_session() as session:
        cities = await db.select_cities(session)
    text = "Выберите город из списка:"
    markup = markups.select_city(cities)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(_callback_data.City.filter(), aiogram.F.message.is_not(None))
async def cq_select_product(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.City,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    await state.update_data(city_id=callback_data.id)
    async with async_session() as session:
        city = await db.select_city(session, callback_data.id)
        products = await db.select_products(session, callback_data.id)
    text = f"<strong>Город:</strong> {city.name}\n\nВыберите товар из списка:"
    markup = markups.select_product(products)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(_callback_data.Product.filter(), aiogram.F.message.is_not(None))
async def cq_select_district(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.Product,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    await state.update_data(product_id=callback_data.id)
    data = await state.get_data()
    city_id: int = data["city_id"]
    async with async_session() as session:
        city = await db.select_city(session, city_id)
        product = await db.select_product(session, callback_data.id)
        districts = await db.select_districts(session, city_id, callback_data.id)
    if product.description is not None and product.description:
        text = (
            f"<strong>Город:</strong> {city.name}\n"
            f"<strong>Товар:</strong> {product.name}\n\n"
            f"<span class='tg-spoiler'>{product.description}</span>\n\n"
            "Выберите район из списка:"
        )
    else:
        text = (
            f"<strong>Город:</strong> {city.name}\n"
            f"<strong>Товар:</strong> {product.name}\n\n"
            "Выберите район из списка:"
        )
    markup = markups.select_district(districts, _callback_data.City(id=city_id))
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(_callback_data.District.filter(), aiogram.F.message.is_not(None))
async def cq_select_product_unit(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.District,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    await state.update_data(district_id=callback_data.id)
    data = await state.get_data()
    city_id: int = data["city_id"]
    product_id: int = data["product_id"]
    async with async_session() as session:
        city = await db.select_city(session, city_id)
        product = await db.select_product(session, product_id)
        district = await db.select_district(session, callback_data.id)
        district_product_units = await db.select_district_product_units(
            session, callback_data.id, product_id
        )
    text = (
        f"<strong>Город:</strong> {city.name}\n"
        f"<strong>Район:</strong> {district.name}\n"
        f"<strong>Товар:</strong> {product.name}\n\n"
        "Выберите фасовку из списка:"
    )
    markup = markups.select_product_unit(
        district_product_units, _callback_data.Product(id=product_id)
    )
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(
    _callback_data.ProductUnit.filter(), aiogram.F.message.is_not(None)
)
async def cq_select_payment_method(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.ProductUnit,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    await state.update_data(product_unit_id=callback_data.id)
    data = await state.get_data()
    city_id: int = data["city_id"]
    product_id: int = data["product_id"]
    district_id: int = data["district_id"]
    async with async_session() as session:
        city = await db.select_city(session, city_id)
        product = await db.select_product(session, product_id)
        district = await db.select_district(session, district_id)
        product_unit = await db.select_product_unit(session, callback_data.id)
        district_product_unit = await db.select_district_product_unit(
            session, district_id, callback_data.id
        )
    text = (
        f"<strong>Город:</strong> {city.name}\n"
        f"<strong>Район:</strong> {district.name}\n"
        f"<strong>Товар:</strong> "
        f"{product.name} {models.ProductUnit.create_str(product_unit)}\n"
        f"<strong>Цена:</strong> {district_product_unit.price}тг\n\n"
        "Выберите способ оплаты из списка:"
    )
    markup = markups.select_payment_method(_callback_data.District(id=district_id))
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)


@router.callback_query(
    _callback_data.PaymentMethod.filter(), aiogram.F.message.is_not(None)
)
async def cq_payment_method(
    callback_query: types.CallbackQuery,
    callback_data: _callback_data.PaymentMethod,
    state: fsm_context.FSMContext,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    await state.update_data(payment_method_name=callback_data.name)
    data = await state.get_data()
    city_id: int = data["city_id"]
    product_id: int = data["product_id"]
    district_id: int = data["district_id"]
    product_unit_id: int = data["product_unit_id"]
    async with async_session() as session:
        city = await db.select_city(session, city_id)
        product = await db.select_product(session, product_id)
        district = await db.select_district(session, district_id)
        product_unit = await db.select_product_unit(session, product_unit_id)
        district_product_unit = await db.select_district_product_unit(
            session, district_id, product_unit_id
        )
    match callback_data.name:
        case _callback_data.PaymentMethodName.BANK:
            payment_method_name = "Банковский перевод"
        case _callback_data.PaymentMethodName.QIWI_WALLET:
            payment_method_name = "QIWI Кошелек"
    text = (
        f"<strong>Город:</strong> {city.name}\n"
        f"<strong>Район:</strong> {district.name}\n"
        f"<strong>Товар:</strong> "
        f"{product.name} {models.ProductUnit.create_str(product_unit)}\n"
        f"<strong>Цена:</strong> {district_product_unit.price}тг\n"
        f"<strong>Способ оплаты:</strong> {payment_method_name}\n\n"
        "Все верно?"
    )
    markup = markups.payment_method_bank(_callback_data.ProductUnit(id=product_unit_id))
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
