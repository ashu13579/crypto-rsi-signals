"""Settings and trading schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SettingsRequest(BaseModel):
    """User settings request"""
    rsi_period: Optional[int] = Field(14, ge=2, le=50)
    rsi_oversold: Optional[int] = Field(30, ge=0, le=50)
    rsi_overbought: Optional[int] = Field(70, ge=50, le=100)
    timeframe: Optional[str] = "1h"
    notifications_enabled: Optional[bool] = True
    exchange_api_key: Optional[str] = None
    exchange_api_secret: Optional[str] = None


class SettingsResponse(BaseModel):
    """User settings response"""
    user_id: str
    rsi_period: int
    rsi_oversold: int
    rsi_overbought: int
    timeframe: str
    notifications_enabled: bool
    has_api_keys: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaperTradeRequest(BaseModel):
    """Paper trade request"""
    symbol: str
    action: str = Field(..., pattern="^(buy|sell)$")
    amount: float = Field(..., gt=0)
    price: Optional[float] = None  # None = market price


class PaperTradeResponse(BaseModel):
    """Paper trade response"""
    trade_id: str
    symbol: str
    action: str
    amount: float
    price: float
    total: float
    timestamp: datetime
    status: str = "executed"
