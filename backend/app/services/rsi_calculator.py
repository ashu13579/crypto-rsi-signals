"""RSI calculation service"""
import pandas as pd
from ta.momentum import RSIIndicator
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RSICalculator:
    """Calculate RSI indicator"""
    
    @staticmethod
    def calculate(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate RSI for given OHLCV dataframe"""
        try:
            if df is None or df.empty:
                raise ValueError("Empty dataframe provided")
            
            if 'close' not in df.columns:
                raise ValueError("Dataframe must contain 'close' column")
            
            rsi_indicator = RSIIndicator(close=df['close'], window=period)
            rsi = rsi_indicator.rsi()
            
            return rsi
            
        except Exception as e:
            logger.error(f"RSI calculation failed: {e}")
            raise
    
    @staticmethod
    def get_current_rsi(df: pd.DataFrame, period: int = 14) -> Optional[float]:
        """Get current RSI value"""
        try:
            rsi = RSICalculator.calculate(df, period)
            return float(rsi.iloc[-1]) if not rsi.empty else None
        except Exception as e:
            logger.error(f"Failed to get current RSI: {e}")
            return None
    
    @staticmethod
    def get_previous_rsi(df: pd.DataFrame, period: int = 14) -> Optional[float]:
        """Get previous RSI value"""
        try:
            rsi = RSICalculator.calculate(df, period)
            return float(rsi.iloc[-2]) if len(rsi) >= 2 else None
        except Exception as e:
            logger.error(f"Failed to get previous RSI: {e}")
            return None
