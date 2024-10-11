import typing
from logging import getLogger
from urllib.parse import quote_plus

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from src.base.unit_of_work import logger


logger = getLogger(__name__)


class CoreSettings(BaseSettings):
    """
    CoreSettings
    """
    app_title: str
    app_version: str
    api_version: str
    app_description: str

    app_port: int = 8080
    app_host: str = "127.0.0.1"
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int | None
    database_url: typing.Optional[str] = None
    log_file: str = "map-box.log"
    root_path: str = ""
    app_env: str = "LOCAL"
    cors_origins_csv: str = "http://127.0.0.1:3000"
    cors_origins: typing.Optional[typing.Set[str]] = None
    current_env: str = "LOCAL"  # This field should be present


    model_config = SettingsConfigDict(env_file=".env")


    @field_validator("database_url")
    def assemble_db_connection(cls, v: typing.Optional[str], info: FieldValidationInfo) -> typing.Any:
        """Generates the database connection URI."""

        if isinstance(v, str):
            return v
        encoded_password = quote_plus(info.data.get("db_password"))
        return (
            f'postgresql://{info.data.get("db_user")}:{encoded_password}@'
            f'{info.data.get("db_host")}@{info.data.get("db_name")}:'
        )

    @field_validator("cors_origins")
    def generate_cors_origins(
            cls, v: typing.Optional[str], info: FieldValidationInfo) -> typing.Set[str]:

        """ """

        if isinstance(v, set):
            logger.info(f"Allowing Origins {v}")
            return v

        cors_csv: str = info.data.get("cors_origins_csv")
        if cors_csv:
            cors_origins = set([item.strip() for item in cors_csv.split(",")])
        else:
            logger.warning(f"No CORS_ORIGIN_CSV variable defined in .env, allowing all origins.")
            cors_origins = {"*"}
        logger.info(f"Allowing Origins {cors_origins}")
        return cors_origins

    @property
    def is_local(self) -> bool:
        """Returns True if the current environment is LOCAL."""
        return self.app_env == "LOCAL"
