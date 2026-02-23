"""Settings and paper trading API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from ..database import get_db
from ..models.user import UserSettings
from ..schemas.settings import (
    SettingsRequest,
    SettingsResponse,
    PaperTradeRequest,
    PaperTradeResponse
)
from ..services.market_data import MarketDataService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=SettingsResponse)
async def update_settings(
    settings: SettingsRequest,
    user_id: str = "default",  # In production, get from auth
    db: Session = Depends(get_db)
):
    """Update user strategy settings"""
    try:
        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        
        if not user_settings:
            user_settings = UserSettings(user_id=user_id)
            db.add(user_settings)
        
        # Update fields
        if settings.rsi_period is not None:
            user_settings.rsi_period = settings.rsi_period
        if settings.rsi_oversold is not None:
            user_settings.rsi_oversold = settings.rsi_oversold
        if settings.rsi_overbought is not None:
            user_settings.rsi_overbought = settings.rsi_overbought
        if settings.timeframe is not None:
            user_settings.timeframe = settings.timeframe
        if settings.notifications_enabled is not None:
            user_settings.notifications_enabled = settings.notifications_enabled
        
        # Handle API keys (should be encrypted in production)
        if settings.exchange_api_key is not None:
            user_settings.exchange_api_key = settings.exchange_api_key
        if settings.exchange_api_secret is not None:
            user_settings.exchange_api_secret = settings.exchange_api_secret
        
        db.commit()
        db.refresh(user_settings)
        
        return SettingsResponse(
            user_id=user_settings.user_id,
            rsi_period=user_settings.rsi_period,
            rsi_oversold=user_settings.rsi_oversold,
            rsi_overbought=user_settings.rsi_overbought,
            timeframe=user_settings.timeframe,
            notifications_enabled=user_settings.notifications_enabled,
            has_api_keys=bool(user_settings.exchange_api_key),
            created_at=user_settings.created_at,
            updated_at=user_settings.updated_at
        )
        
    except Exception as e:
        logger.error(f"Failed to update settings: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update settings")


@router.get("", response_model=SettingsResponse)
async def get_settings(
    user_id: str = "default",
    db: Session = Depends(get_db)
):
    """Get user settings"""
    try:
        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        
        if not user_settings:
            # Return default settings
            from ..config import settings as app_settings
            return SettingsResponse(
                user_id=user_id,
                rsi_period=app_settings.default_rsi_period,
                rsi_oversold=app_settings.default_rsi_oversold,
                rsi_overbought=app_settings.default_rsi_overbought,
                timeframe=app_settings.default_timeframe,
                notifications_enabled=True,
                has_api_keys=False,
                created_at=datetime.now(),
                updated_at=None
            )
        
        return SettingsResponse(
            user_id=user_settings.user_id,
            rsi_period=user_settings.rsi_period,
            rsi_oversold=user_settings.rsi_oversold,
            rsi_overbought=user_settings.rsi_overbought,
            timeframe=user_settings.timeframe,
            notifications_enabled=user_settings.notifications_enabled,
            has_api_keys=bool(user_settings.exchange_api_key),
            created_at=user_settings.created_at,
            updated_at=user_settings.updated_at
        )
        
    except Exception as e:
        logger.error(f"Failed to get settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to get settings")


@router.post("/paper-trade", response_model=PaperTradeResponse)
async def execute_paper_trade(
    trade: PaperTradeRequest,
    db: Session = Depends(get_db)
):
    """Execute paper trade (simulation)"""
    try:
        market_service = MarketDataService()
        
        # Get current price if not provided
        if trade.price is None:
            ticker = await market_service.fetch_ticker(trade.symbol)
            price = ticker['price']
        else:
            price = trade.price
        
        # Calculate total
        total = trade.amount * price
        
        # Generate trade ID
        trade_id = str(uuid.uuid4())
        
        # In production, store this in database
        logger.info(f"Paper trade executed: {trade.action} {trade.amount} {trade.symbol} @ {price}")
        
        return PaperTradeResponse(
            trade_id=trade_id,
            symbol=trade.symbol,
            action=trade.action,
            amount=trade.amount,
            price=price,
            total=total,
            timestamp=datetime.now(),
            status="executed"
        )
        
    except Exception as e:
        logger.error(f"Failed to execute paper trade: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute paper trade: {str(e)}")
