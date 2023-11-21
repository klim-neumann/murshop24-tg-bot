import sqlalchemy as sqla
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _settings

_ENGINE_DRIVER = "postgresql+psycopg"


def create_async_engine() -> sqla_asyncio.AsyncEngine:
    postgres_settings = _settings.PostgresSettings()  # type: ignore
    url = sqla.URL.create(
        _ENGINE_DRIVER,
        username=postgres_settings.user,
        password=postgres_settings.password,
        host=postgres_settings.host,
        port=postgres_settings.port,
        database=postgres_settings.db,
    )
    return sqla_asyncio.create_async_engine(url, echo=False)
