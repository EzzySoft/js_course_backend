from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    trips: str = "/trips"
    google: str = "/auth/google"
    chat: str = "/chat"
    cars: str = "/cars"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()




class DatabaseConfig(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    echo: bool = True
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50
    tags: list[str] = ["smoke", "child", "parcels", "with_animals", "max_two", "only_verified"]

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    model_config = ConfigDict(extra="ignore")


class ValidationConfig(BaseModel):
    email_pattern: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class GeocoderConfig(BaseModel):
    api_key: str
    url: str
    path_api_key: str


class RedisConfig(BaseModel):
    host: str = "localhost"
    expire_time: int = 3600


class GoogleConfig(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=".env"
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    database: DatabaseConfig
    redis: RedisConfig
    validation: ValidationConfig = ValidationConfig()
    BaseSettings.model_config = ConfigDict(extra="ignore")


settings = Settings()
