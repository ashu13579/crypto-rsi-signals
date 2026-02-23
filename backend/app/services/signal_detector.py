"""Signal detection service"""
import pandas as pd
from typing import Optional
from ..models.signal import SignalType
from .rsi_calculator import RSICalculator
import logging

logger = logging.getLogger(__name__)


class SignalDetector:
    """Detect trading signals based on RSI"""
    
    def __init__(self, oversold: int = 30, overbought: int = 70, period: int = 14):
        """Initialize signal detector"""
        self.oversold = oversold
        self.overbought = overbought
        self.period = period
    
    def detect_signal(self, df: pd.DataFrame) -> tuple[SignalType, float]:
        """Detect signal from OHLCV data
        
        Returns:
            tuple: (signal_type, current_rsi)
        """
        try:
            current_rsi = RSICalculator.get_current_rsi(df, self.period)
            previous_rsi = RSICalculator.get_previous_rsi(df, self.period)
            
            if current_rsi is None or previous_rsi is None:
                return SignalType.HOLD, 50.0
            
            # BUY signal: RSI crosses above oversold level
            if previous_rsi <= self.oversold and current_rsi > self.oversold:
                logger.info(f"BUY signal detected: RSI {previous_rsi:.2f} -> {current_rsi:.2f}")
                return SignalType.BUY, current_rsi
            
            # SELL signal: RSI crosses below overbought level
            if previous_rsi >= self.overbought and current_rsi < self.overbought:
                logger.info(f"SELL signal detected: RSI {previous_rsi:.2f} -> {current_rsi:.2f}")
                return SignalType.SELL, current_rsi
            
            # HOLD: No signal
            return SignalType.HOLD, current_rsi
            
        except Exception as e:
            logger.error(f"Signal detection failed: {e}")
            return SignalType.HOLD, 50.0
    
    def is_oversold(self, rsi: float) -> bool:
        """Check if RSI indicates oversold condition"""
        return rsi <= self.oversold
    
    def is_overbought(self, rsi: float) -> bool:
        """Check if RSI indicates overbought condition"""
        return rsi >= self.overbought
