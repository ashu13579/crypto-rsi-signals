"""User settings database model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base


class UserSettings(Base):
    """User settings model"""
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    rsi_period = Column(Integer, default=14)
    rsi_oversold = Column(Integer, default=30)
    rsi_overbought = Column(Integer, default=70)
    timeframe = Column(String, default="1h")
    notifications_enabled = Column(Boolean, default=True)
    exchange_api_key = Column(String, nullable=True)  # Encrypted
    exchange_api_secret = Column(String, nullable=True)  # Encrypted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserSettings {self.user_id}>"
