from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 63791
    password: str = None


class SecretSettings(BaseSettings):
    mysql_username: str
    mysql_password: str
    mysql_host: str
    mysql_dbname: str
    mysql_port: int
    redis: RedisSettings = RedisSettings()

    class Config:
        env_file = f"./.env.test"


secret_settings = SecretSettings()
