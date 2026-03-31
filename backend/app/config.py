from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://cashflow:cashflow_dev@localhost:5432/cashflow_ai"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440

    # CORS
    CORS_ORIGINS: str = "http://localhost:9999"

    # M-Pesa
    MPESA_CONSUMER_KEY: str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_SHORTCODE: str = "174379"
    MPESA_PASSKEY: str = ""
    MPESA_CALLBACK_URL: str = ""
    MPESA_ENV: str = "sandbox"

    # Ratiba
    RATIBA_API_KEY: str = ""
    RATIBA_BASE_URL: str = "https://api.ratiba.io"
    RATIBA_WEBHOOK_URL: str = ""

    # OpenRouter AI
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-001"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # Africa's Talking
    AT_API_KEY: str = ""
    AT_USERNAME: str = "sandbox"
    AT_SENDER_ID: str = ""

    # eSMS Mail
    ESMS_API_KEY: str = ""
    ESMS_BASE_URL: str = "https://send.esmsafrica.io"
    ESMS_FROM_EMAIL: str = "hello@flowai.cash"
    ESMS_FROM_NAME: str = "CashFlow AI"
    APP_URL: str = "https://flowai.cash"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
