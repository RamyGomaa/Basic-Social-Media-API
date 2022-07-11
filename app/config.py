from pydantic import BaseSettings

class Settings(BaseSettings):
   
    DB_DRIVER: str 
    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str
    DB_USER: str 
    DB_PASSWORD:str
    DB_URL: str = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()