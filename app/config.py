from pydantic import BaseSettings


class Settings(BaseSettings):
    db_pass: str
    db_port: str
    db_name: str
    db_username: str
    db_hostname: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
