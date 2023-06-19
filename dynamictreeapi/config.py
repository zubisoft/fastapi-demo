from pydantic import BaseSettings


class Settings (BaseSettings):
    db_hostname: str
    db_user:str
    db_pass:str
    db_name:str
    db_port:str
    jwt_secret_key:str
    jwt_algorithm:str

    class Config:
        env_file = '.env'



settings = Settings()