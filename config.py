from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    post_limit: int = 10000

    class Config:
        env_file = ".env"


settings = Settings()
