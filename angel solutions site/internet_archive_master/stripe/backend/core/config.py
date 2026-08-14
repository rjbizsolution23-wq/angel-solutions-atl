from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Stripe Configuration
    stripe_secret_key_test: str = ""
    stripe_secret_key_live: str = ""
    stripe_publishable_key_test: str = ""
    stripe_publishable_key_live: str = ""
    stripe_webhook_secret: str = ""
    
    # Google AI
    google_ai_api_key: str
    
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str = ""
    
    # App Configuration
    environment: str = "development"
    stripe_mode: str = "test"  # "test" or "live"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def stripe_secret_key(self) -> str:
        """Get the appropriate Stripe secret key based on mode."""
        if self.stripe_mode == "live":
            return self.stripe_secret_key_live
        return self.stripe_secret_key_test
    
    @property
    def stripe_publishable_key(self) -> str:
        """Get the appropriate Stripe publishable key based on mode."""
        if self.stripe_mode == "live":
            return self.stripe_publishable_key_live
        return self.stripe_publishable_key_test


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
