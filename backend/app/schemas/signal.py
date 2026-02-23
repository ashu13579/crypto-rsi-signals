"""Signal schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from ..models.signal import SignalType


class SignalBase(BaseModel):
    """Base signal schema"""
    symbol: str
    signal_type: SignalType
    rsi_value: float = Field(..., ge=0, le=100)
    price: float = Field(..., gt=0)
    timeframe: str = "1h"


class SignalResponse(SignalBase):
    """Signal response schema"""
    id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class SignalListResponse(BaseModel):
    """List of signals response"""
    signals: List[SignalResponse]
    total: int
    page: int = 1
    page_size: int = 50


class MarketDataResponse(BaseModel):
    """Market data response"""
    symbol: str
    price: float
    rsi: float
    signal: SignalType
    change_24h: Optional[float] = None
    volume_24h: Optional[float] = None
    timestamp: datetime
