"""Background signal scanner"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.signal import Signal
from ..services.market_data import MarketDataService
from ..services.signal_detector import SignalDetector
from ..services.rsi_calculator import RSICalculator
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class SignalScanner:
    """Background scanner for detecting signals"""
    
    def __init__(self):
        self.market_service = MarketDataService()
        self.detector = SignalDetector(
            oversold=settings.default_rsi_oversold,
            overbought=settings.default_rsi_overbought,
            period=settings.default_rsi_period
        )
        self.running = False
    
    async def scan_symbol(self, symbol: str, db: Session):
        """Scan single symbol for signals"""
        try:
            # Fetch OHLCV data
            df = await self.market_service.fetch_ohlcv(
                symbol,
                settings.default_timeframe
            )
            
            # Detect signal
            signal_type, rsi_value = self.detector.detect_signal(df)
            
            # Get current price
            ticker = await self.market_service.fetch_ticker(symbol)
            price = ticker['price']
            
            # Store signal in database
            signal = Signal(
                symbol=symbol,
                signal_type=signal_type,
                rsi_value=rsi_value,
                price=price,
                timeframe=settings.default_timeframe,
                timestamp=datetime.now()
            )
            
            db.add(signal)
            db.commit()
            
            logger.info(f"Scanned {symbol}: {signal_type} (RSI: {rsi_value:.2f}, Price: {price:.2f})")
            
        except Exception as e:
            logger.error(f"Failed to scan {symbol}: {e}")
            db.rollback()
    
    async def scan_all_symbols(self):
        """Scan all configured symbols"""
        db = SessionLocal()
        try:
            logger.info(f"Starting scan of {len(settings.symbols_list)} symbols")
            
            for symbol in settings.symbols_list:
                await self.scan_symbol(symbol, db)
                await asyncio.sleep(0.5)  # Rate limiting
            
            logger.info("Scan completed")
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
        finally:
            db.close()
    
    async def start(self):
        """Start continuous scanning"""
        self.running = True
        logger.info(f"Signal scanner started (interval: {settings.scan_interval_seconds}s)")
        
        while self.running:
            try:
                await self.scan_all_symbols()
                await asyncio.sleep(settings.scan_interval_seconds)
            except Exception as e:
                logger.error(f"Scanner error: {e}")
                await asyncio.sleep(10)  # Wait before retry
    
    def stop(self):
        """Stop scanner"""
        self.running = False
        logger.info("Signal scanner stopped")
