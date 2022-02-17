from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import String

from models import get_ticker_table

from . import models, schemas


def get_history(db: Session, start: String, end: String, interval: String):
    """
    summary: Get history between start to end date in the db. 

    Example:
        from app.db.session import SessionLocal // update according to the current position
        db = SessionLocal()
        start = '2020-01-01'
        end = '2020-01-31'
        history = get_history(db, start, end)
    
    !IMPORTANT
        start, end date format must be 'YYYY-MM-DD'
    """
    ticker_table = get_ticker_table(interval)
    history = db.query(ticker_table).filter(ticker_table.date >= start, ticker_table.date <= end).all()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

def create_history(db: Session, history, interval: String):
    """
    summary: Save ticker history to db.

    Example: 
        from app.db.session import SessionLocal // update according to the current position
        from datetime import datetime

        db = SessionLocal()
        item = {'date': '2020-01-02T00:00:00.000Z', 'open': 73.1920046399, 'high': 74.2692336173, 'low': 72.9325841905, 'close': 74.2074661255, 'volume': 135480400, 'dividends': 0, 'stock_splits': 0}
        item.date = datetime.fromisoformat(item['date'][:-1] + '+00:00').date()

        history = create_history(db, item)
    """
    ticker_table = get_ticker_table(interval)
    data = ticker_table(**history)
    db.add(data)
    db.commit()
    return data

def get_history_count(db: Session, start: String, end: String, interval: String):
    """
    summary: Get number of history between start to end date in the db. 

    Example:
        from app.db.session import SessionLocal // update according to the current position
        db = SessionLocal()
        start = '2020-01-01'
        end = '2020-01-31'
        history = get_history_count(db, start, end)
    
    !IMPORTANT
        start, end date format must be 'YYYY-MM-DD'
    """
    ticker_table = get_ticker_table(interval)

    count = db.query(ticker_table).filter(ticker_table.date >= start, ticker_table.date <= end).count()
    return count