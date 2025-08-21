from pydantic import computed_field, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,  # Ignore empty fields in the environment file
        extra="ignore"  # Ignore extra fields in the environment file
    )
    
    # Application Configuration
    TITLE: str = "URL Shortener API"
    DESCRIPTION: str = "A simple URL shortener API built with FastAPI and SQLModel."
    VERSION: str = "1.0.0"
    
    HOST_URL: str = "http://localhost:8000"  # Base URL for the application
    
    EXPIRATION_TIME: int = 7  # Default expiration time in days for shortened URLs
    
    API_V1_STR: str = "/api/v1"
    
    REDIS_HOST: str = "localhost"  # Redis host for rate limiting
    REDIS_PORT: int = 6379  # Redis port for rate limiting
    REDIS_DB: int = 0
    REDIS_USER: str = "default"
    REDIS_PASSWORD: str = "your_redis_password"
    RATE_LIMIT_WINDOW: int = 60  # Rate limit window in seconds
    RATE_LIMIT_MAX_REQUESTS: int = 10

    # MySQL Database Configuration
    # Replace with your actual MySQL credentials
    
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "urlDB"
    
    @computed_field(return_type=str)
    @property
    def MYSQL_DATABASE_URI(self):
        if not all([self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_HOST, self.MYSQL_PORT, self.MYSQL_DB]):
            raise ValueError("MySQL configuration is incomplete. Please check your .env file.")
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
    
    
settings = Settings()