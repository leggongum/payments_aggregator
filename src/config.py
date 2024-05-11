from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    BOT_TOKEN: str
    WEBAPP_URL: str = '127.0.0.1:3000'

    MONGODB_URL: str 

    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
