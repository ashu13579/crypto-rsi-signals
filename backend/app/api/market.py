"""Market data API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..services.market_data import MarketDataService
from ..services.rsi_calculator import RSICalculator
from ..services.signal_detector import SignalDetector
from ..schemas.signal import MarketDataResponse
from ..config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{symbol}", response_model=MarketDataResponse)
async def get_market_data(
    symbol: str,
    timeframe: str = "1h",
    db: Session = Depends(get_db)
):
    """Get latest market data with RSI and signal"""
    try:
        market_service = MarketDataService()
        
        # Fetch OHLCV data
        df = await market_service.fetch_ohlcv(symbol, timeframe)
        
        # Calculate RSI
        current_rsi = RSICalculator.get_current_rsi(df, settings.default_rsi_period)
        
        # Detect signal
        detector = SignalDetector(
            oversold=settings.default_rsi_oversold,
            overbought=settings.default_rsi_overbought,
            period=settings.default_rsi_period
        )
        signal_type, _ = detector.detect_signal(df)
        
        # Get ticker data
        ticker = await market_service.fetch_ticker(symbol)
        
        return MarketDataResponse(
            symbol=symbol,
            price=ticker['price'],
            rsi=current_rsi or 50.0,
            signal=signal_type,
            change_24h=ticker.get('change_24h'),
            volume_24h=ticker.get('volume_24h'),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Failed to fetch market data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch market data: {str(e)}")


@router.get("/overview/all", response_model=List[MarketDataResponse])
async def get_market_overview(
    timeframe: str = "1h",
    db: Session = Depends(get_db)
):
    """Get market overview for all tracked symbols"""
    try:
        market_service = MarketDataService()
        detector = SignalDetector(
            oversold=settings.default_rsi_oversold,
            overbought=settings.default_rsi_overbought,
            period=settings.default_rsi_period
        )
        
        results = []
        
        for symbol in settings.symbols_list:
            try:
                # Fetch data
                df = await market_service.fetch_ohlcv(symbol, timeframe)
                ticker = await market_service.fetch_ticker(symbol)
                
                # Calculate RSI and signal
                current_rsi = RSICalculator.get_current_rsi(df, settings.default_rsi_period)
                signal_type, _ = detector.detect_signal(df)
                
                results.append(MarketDataResponse(
                    symbol=symbol,
                    price=ticker['price'],
                    rsi=current_rsi or 50.0,
                    signal=signal_type,
                    change_24h=ticker.get('change_24h'),
                    volume_24h=ticker.get('volume_24h'),
                    timestamp=datetime.now()
                ))
                
            except Exception as e:
                logger.warning(f"Skipping {symbol}: {e}")
                continue
        
        return results
        
    except Exception as e:
        logger.error(f"Failed to fetch market overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch market overview")
