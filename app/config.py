from pydantic_settings import BaseSettings
from pydantic import AnyUrl
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URL_DEV: AnyUrl
    DATABASE_URL_PREPROD: AnyUrl
    DATABASE_URL_PROD: AnyUrl

    # Determine the database URL based on the environment
    @property
    def DATABASE_URL(self):
        if self.ENVIRONMENT == "development":
            return self.DATABASE_URL_DEV
        elif self.ENVIRONMENT == "preprod":
            return self.DATABASE_URL_PREPROD
        elif self.ENVIRONMENT == "prod":
            return self.DATABASE_URL_PROD
        else:
            raise ValueError("Invalid environment")

    class Config:
        env_file = ".env"

settings = Settings()
