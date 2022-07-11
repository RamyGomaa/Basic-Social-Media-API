from pydantic import BaseSettings

class Settings(BaseSettings):
   
    DATABASE_DRIVER: str 
    DATABASE_HOSTNAME: str 
    DATABASE_PORT: int 
    DATABASE_NAME: str
    DATABASE_USERNAME: str 
    DATABASE_PASSWORD:str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    class Config:
        env_file = ".env"
    
    
    
settings = Settings()

# = f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"