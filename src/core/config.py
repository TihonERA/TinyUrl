from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn, RedisDsn, computed_field
from pydantic.networks import AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(default=...)
    POSTGRES_PORT: int = Field(default=...)
    POSTGRES_USER: str = Field(default=...)
    POSTGRES_PASS: str = Field(default=...)
    POSTGRES_NAME: str = Field(default=...)

    REDIS_HOST: str = Field(default=...)
    REDIS_PORT: int = Field(default=...)

    RABBITMQ_HOST: str = Field(default=...)
    RABBITMQ_PORT: int = Field(default=...)
    RABBITMQ_USER: str = Field(default=...)
    RABBITMQ_PASS: str = Field(default=...)

    SECRET_KEY: str = Field(default=...)
    ALGORITHM: str = Field(default=...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=...)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=...)
    ORIGINS: list[str] = Field(default=...)

    @computed_field
    @property
    def POSTGRES_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASS,
            path=self.POSTGRES_NAME,
        )

    @computed_field
    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis", host=self.REDIS_HOST, port=self.REDIS_PORT
        )

    @computed_field
    @property
    def RABBITMQ_URL(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
            username=self.RABBITMQ_USER,
            password=self.RABBITMQ_PASS,
        )

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
