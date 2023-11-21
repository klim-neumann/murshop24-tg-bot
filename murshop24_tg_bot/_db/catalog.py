from typing import Sequence

import murshop24_models as models  # type: ignore
import sqlalchemy as sqla
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _errors


async def select_cities(session: sqla_asyncio.AsyncSession) -> Sequence[models.City]:
    stmt = (
        sqla.select(models.City)
        .join(models.District)
        .join(models.DistrictProductUnit)
        .distinct()
    )
    cities = (await session.scalars(stmt)).all()
    if not cities:
        raise _errors.TgBotError()
    return cities


async def select_city(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.City:
    stmt = sqla.select(models.City).where(models.City.id == id)
    city = await session.scalar(stmt)
    if city is None:
        raise _errors.TgBotError()
    return city


async def select_products(
    session: sqla_asyncio.AsyncSession, city_id: int
) -> Sequence[models.Product]:
    stmt = (
        sqla.select(models.Product)
        .join(models.ProductUnit)
        .join(models.DistrictProductUnit)
        .join(models.District)
        .where(models.District.city_id == city_id)
        .distinct()
    )
    products = (await session.scalars(stmt)).all()
    if not products:
        raise _errors.TgBotError()
    return products


async def select_product(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.Product:
    stmt = sqla.select(models.Product).where(models.Product.id == id)
    product = await session.scalar(stmt)
    if product is None:
        raise _errors.TgBotError()
    return product


async def select_districts(
    session: sqla_asyncio.AsyncSession, city_id: int, product_id: int
) -> Sequence[models.District]:
    stmt = (
        sqla.select(models.District)
        .join(models.DistrictProductUnit)
        .join(models.ProductUnit)
        .join(models.Product)
        .where(models.District.city_id == city_id, models.Product.id == product_id)
        .distinct()
    )
    districts = (await session.scalars(stmt)).all()
    if not districts:
        raise _errors.TgBotError()
    return districts


async def select_district(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.District:
    stmt = sqla.select(models.District).where(models.District.id == id)
    district = await session.scalar(stmt)
    if district is None:
        raise _errors.TgBotError()
    return district


async def select_district_product_units(
    session: sqla_asyncio.AsyncSession, district_id: int, product_id: int
) -> Sequence[models.DistrictProductUnit]:
    stmt = (
        sqla.select(models.DistrictProductUnit)
        .join(models.ProductUnit)
        .where(
            models.DistrictProductUnit.district_id == district_id,
            models.ProductUnit.product_id == product_id,
        )
        .options(orm.selectinload(models.DistrictProductUnit.product_unit))
    )
    district_product_units = (await session.scalars(stmt)).all()
    if not district_product_units:
        raise _errors.TgBotError()
    return district_product_units


async def select_district_product_unit(
    session: sqla_asyncio.AsyncSession, district_id: int, product_unit_id: int
) -> models.DistrictProductUnit:
    stmt = sqla.select(models.DistrictProductUnit).where(
        models.DistrictProductUnit.district_id == district_id,
        models.DistrictProductUnit.product_unit_id == product_unit_id,
    )
    district_product_unit = await session.scalar(stmt)
    if district_product_unit is None:
        raise _errors.TgBotError()
    return district_product_unit


async def select_product_unit(
    session: sqla_asyncio.AsyncSession, id: int
) -> models.ProductUnit:
    stmt = sqla.select(models.ProductUnit).where(models.ProductUnit.id == id)
    product_unit = await session.scalar(stmt)
    if product_unit is None:
        raise _errors.TgBotError()
    return product_unit


async def select_bank_account(
    session: sqla_asyncio.AsyncSession,
) -> models.BankAccount:
    stmt = sqla.select(models.BankAccount)
    bank_account = await session.scalar(stmt)
    if bank_account is None:
        raise _errors.TgBotError()
    return bank_account


async def select_qiwi_wallet_account(
    session: sqla_asyncio.AsyncSession,
) -> models.QiwiWalletAccount:
    stmt = sqla.select(models.QiwiWalletAccount)
    qiwi_wallet_account = await session.scalar(stmt)
    if qiwi_wallet_account is None:
        raise _errors.TgBotError()
    return qiwi_wallet_account
