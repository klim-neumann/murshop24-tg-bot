import pydantic_settings


class PostgresSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="postgres_")
    password: str
    user: str = "postgres"
    db: str = user
    host: str = "localhost"
    port: int = 5432


class RedisSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="redis_")
    host: str = "localhost"
    port: int = 6379


class TgBotSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="tg_bot_")
    secret_token: str
