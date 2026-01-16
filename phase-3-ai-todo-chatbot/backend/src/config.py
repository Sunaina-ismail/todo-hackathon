"""Application Configuration

Settings loaded from environment variables using pydantic-settings.
"""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Database Configuration
    DATABASE_URL: str

    # Authentication Configuration
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 604800  # 7 days in seconds

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Configuration (comma-separated string in .env)
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # Neon Database Pool Configuration (Serverless Optimized)
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 300  # 5 minutes

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
