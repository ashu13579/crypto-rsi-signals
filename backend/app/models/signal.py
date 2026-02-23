"""Signal database model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from ..database import Base
import enum


class SignalType(str, enum.Enum):
    """Signal type enumeration"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class Signal(Base):
    """Signal model for storing trading signals"""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    signal_type = Column(Enum(SignalType), nullable=False)
    rsi_value = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timeframe = Column(String, default="1h")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Signal {self.symbol} {self.signal_type} @ {self.price}>"
