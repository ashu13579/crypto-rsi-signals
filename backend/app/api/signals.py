"""Signal API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from ..database import get_db
from ..models.signal import Signal, SignalType
from ..schemas.signal import SignalResponse, SignalListResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=SignalListResponse)
async def get_signals(
    symbol: Optional[str] = None,
    signal_type: Optional[SignalType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get latest signals with optional filtering"""
    try:
        query = db.query(Signal)
        
        if symbol:
            query = query.filter(Signal.symbol == symbol)
        
        if signal_type:
            query = query.filter(Signal.signal_type == signal_type)
        
        total = query.count()
        
        signals = query.order_by(desc(Signal.timestamp)).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        return SignalListResponse(
            signals=signals,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to fetch signals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch signals")


@router.get("/active", response_model=List[SignalResponse])
async def get_active_signals(
    db: Session = Depends(get_db)
):
    """Get latest active signals (one per symbol)"""
    try:
        # Get latest signal for each symbol
        subquery = db.query(
            Signal.symbol,
            func.max(Signal.timestamp).label('max_timestamp')
        ).group_by(Signal.symbol).subquery()
        
        signals = db.query(Signal).join(
            subquery,
            (Signal.symbol == subquery.c.symbol) & 
            (Signal.timestamp == subquery.c.max_timestamp)
        ).filter(
            Signal.signal_type != SignalType.HOLD
        ).all()
        
        return signals
        
    except Exception as e:
        logger.error(f"Failed to fetch active signals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch active signals")


@router.get("/{symbol}", response_model=SignalListResponse)
async def get_symbol_signals(
    symbol: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get signal history for specific symbol"""
    try:
        query = db.query(Signal).filter(Signal.symbol == symbol)
        total = query.count()
        
        signals = query.order_by(desc(Signal.timestamp)).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        
        return SignalListResponse(
            signals=signals,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to fetch signals for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch signals for {symbol}")
