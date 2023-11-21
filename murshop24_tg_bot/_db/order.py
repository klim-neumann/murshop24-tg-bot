from collections.abc import Sequence

import murshop24_models as models  # type: ignore
import sqlalchemy as sqla
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sqla_asyncio
from murshop24_models import enums as model_enums  # type: ignore

from murshop24_tg_bot import _errors


async def select_tg_customer(
    session: sqla_asyncio.AsyncSession, tg_id: int
) -> models.TgCustomer:
    stmt = sqla.select(models.TgCustomer).where(models.TgCustomer.tg_id == tg_id)
    tg_customer = await session.scalar(stmt)
    if tg_customer is None:
        raise _errors.TgBotError()
    return tg_customer


async def select_orders(
    session: sqla_asyncio.AsyncSession, tg_id: int
) -> Sequence[models.Order]:
    stmt = (
        sqla.select(models.Order)
        .join(models.TgCustomer)
        .where(models.TgCustomer.tg_id == tg_id)
        .order_by(models.Order.created_at.desc())
        .limit(12)
    )
    return (await session.scalars(stmt)).all()


async def select_order(session: sqla_asyncio.AsyncSession, id: int) -> models.Order:
    stmt = (
        sqla.select(models.Order)
        .where(models.Order.id == id)
        .options(
            orm.selectinload(models.Order.district),
            orm.selectinload(models.Order.product_unit),
            orm.selectinload(models.Order.bank_account),
            orm.selectinload(models.Order.qiwi_wallet_account),
        )
    )
    order = await session.scalar(stmt)
    if order is None:
        raise _errors.TgBotError()
    return order


async def insert_order(
    session: sqla_asyncio.AsyncSession,
    tg_customer: models.TgCustomer,
    district: models.District,
    product_unit: models.ProductUnit,
    bank_account: models.BankAccount | None = None,
    qiwi_wallet_account: models.QiwiWalletAccount | None = None,
) -> models.Order:
    select_district_product_unit_stmt = sqla.select(models.DistrictProductUnit).where(
        models.DistrictProductUnit.district_id == district.id,
        models.DistrictProductUnit.product_unit_id == product_unit.id,
    )
    district_product_unit = await session.scalar(select_district_product_unit_stmt)
    if district_product_unit is None:
        raise _errors.TgBotError()
    stmt = (
        sqla.insert(models.Order)
        .values(
            price=district_product_unit.price,
            tg_customer_id=tg_customer.id,
            district_id=district.id,
            product_unit_id=product_unit.id,
            bank_account_id=bank_account.id if bank_account is not None else None,
            qiwi_wallet_account_id=qiwi_wallet_account.id
            if qiwi_wallet_account is not None
            else None,
        )
        .returning(models.Order)
    )
    order = await session.scalar(stmt)
    if order is None:
        raise _errors.TgBotError()
    return order


async def cancel_order(session: sqla_asyncio.AsyncSession, id: int) -> None:
    stmt = (
        sqla.update(models.Order)
        .where(models.Order.id == id)
        .values(status=model_enums.OrderStatus.CANCELED)
    )
    await session.execute(stmt)


async def confirm_order(session: sqla_asyncio.AsyncSession, id: int) -> None:
    stmt = (
        sqla.update(models.Order)
        .where(models.Order.id == id)
        .values(status=model_enums.OrderStatus.PAYMENT_CHECKING)
    )
    await session.execute(stmt)


async def select_city(
    session: sqla_asyncio.AsyncSession, district_id: int
) -> models.City:
    stmt = (
        sqla.select(models.City)
        .join(models.District)
        .where(models.District.id == district_id)
    )
    city = await session.scalar(stmt)
    if city is None:
        raise _errors.TgBotError()
    return city


async def select_district(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.District:
    stmt = sqla.select(models.District).where(models.District.id == id)
    district = await session.scalar(stmt)
    if district is None:
        raise _errors.TgBotError()
    return district


async def select_product(
    session: sqla_asyncio.AsyncSession, product_unit_id: int
) -> models.City:
    stmt = (
        sqla.select(models.Product)
        .join(models.ProductUnit)
        .where(models.ProductUnit.id == product_unit_id)
    )
    product = await session.scalar(stmt)
    if product is None:
        raise _errors.TgBotError()
    return product


async def select_product_unit(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.ProductUnit:
    stmt = sqla.select(models.ProductUnit).where(models.ProductUnit.id == id)
    product_unit = await session.scalar(stmt)
    if product_unit is None:
        raise _errors.TgBotError()
    return product_unit


async def select_district_product_unit(
    session: sqla_asyncio.AsyncSession, district_id: int, product_unit_id: int
) -> models.City:
    stmt = sqla.select(models.DistrictProductUnit).where(
        models.DistrictProductUnit.district_id == district_id,
        models.DistrictProductUnit.product_unit_id == product_unit_id,
    )
    district_product_unit = await session.scalar(stmt)
    if district_product_unit is None:
        raise _errors.TgBotError()
    return district_product_unit
