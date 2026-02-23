"""Market data service using CCXT"""
import ccxt
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class MarketDataService:
    """Service for fetching market data from exchanges"""
    
    def __init__(self, exchange_name: str = None):
        """Initialize market data service"""
        exchange_name = exchange_name or settings.default_exchange
        
        try:
            exchange_class = getattr(ccxt, exchange_name)
            self.exchange = exchange_class({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                }
            })
            
            if settings.exchange_testnet:
                self.exchange.set_sandbox_mode(True)
                
        except Exception as e:
            logger.error(f"Failed to initialize exchange {exchange_name}: {e}")
            raise
    
    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data for a symbol"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            raise
    
    async def fetch_ticker(self, symbol: str) -> Dict:
        """Fetch current ticker data"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'change_24h': ticker.get('percentage'),
                'volume_24h': ticker.get('quoteVolume'),
                'timestamp': datetime.fromtimestamp(ticker['timestamp'] / 1000)
            }
        except Exception as e:
            logger.error(f"Failed to fetch ticker for {symbol}: {e}")
            raise
    
    async def fetch_multiple_tickers(self, symbols: List[str]) -> List[Dict]:
        """Fetch tickers for multiple symbols"""
        results = []
        for symbol in symbols:
            try:
                ticker = await self.fetch_ticker(symbol)
                results.append(ticker)
            except Exception as e:
                logger.warning(f"Skipping {symbol}: {e}")
                continue
        return results
    
    def get_available_symbols(self) -> List[str]:
        """Get list of available trading symbols"""
        try:
            markets = self.exchange.load_markets()
            return [symbol for symbol in markets.keys() if '/USDT' in symbol]
        except Exception as e:
            logger.error(f"Failed to load markets: {e}")
            return []
