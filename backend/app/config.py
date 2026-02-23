"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Crypto RSI Signals"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./crypto_rsi.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Exchange
    default_exchange: str = "binance"
    exchange_testnet: bool = False
    
    # RSI Settings
    default_rsi_period: int = 14
    default_rsi_oversold: int = 30
    default_rsi_overbought: int = 70
    default_timeframe: str = "1h"
    
    # Scanner
    scan_interval_seconds: int = 60
    default_symbols: str = "BTC/USDT,ETH/USDT,BNB/USDT,XRP/USDT,ADA/USDT,SOL/USDT,DOT/USDT,DOGE/USDT,AVAX/USDT,MATIC/USDT,LINK/USDT,UNI/USDT,ATOM/USDT,LTC/USDT,ETC/USDT,XLM/USDT,ALGO/USDT,VET/USDT,FIL/USDT,TRX/USDT"
    
    @property
    def symbols_list(self) -> List[str]:
        return [s.strip() for s in self.default_symbols.split(",")]
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_enabled: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
