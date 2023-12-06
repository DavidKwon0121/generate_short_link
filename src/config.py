import os

from pydantic_settings import BaseSettings


def is_on_pytest():
    return os.getenv("ENV", False) == "TEST"


class SecretSettings(BaseSettings):
    mysql_username: str
    mysql_password: str
    mysql_host: str
    mysql_dbname: str
    mysql_port: int

    redis_host: str
    redis_port: int

    class Config:
        env_file = "./.env.test" if is_on_pytest() else "./.env"


secret_settings = SecretSettings()
