from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import String
from sqlalchemy import asc

from app.db.models import get_ticker_table

def get_history(db: Session, symbol: String, start: String, end: String, interval: String):
    """
    Get history between start to end date in the db. 
    :param db: data base connection session
    :param symbol: ticker symbol for which being searched
    :param start: date from which start search
    :param end: date to which start search
    :param interval: search intensity which is one of '1d', '1w' and '1mo'

    :return list of TickerHistory in ascending order

    Example:
        from app.db.session import SessionLocal // update according to the current position
        db = SessionLocal()
        start = '2020-01-01'
        end = '2020-01-31'
        history = get_history(db,'aapl' ,start, end, '1d')
    
    !IMPORTANT
        start, end date format must be 'YYYY-MM-DD'
    """
    ticker_table = get_ticker_table(interval)
    history = db.query(ticker_table).filter(ticker_table.date > start, ticker_table.date < end, ticker_table.symbol == symbol).order_by(asc(ticker_table.date)).all()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

def create_history(db: Session, history, interval: String):
    """
    Save ticker history to db.
    :param db: data base connection session
    :param history: history item standing for the interval, i.e data for one day
    :param interval: search intensity which is one of '1d', '1w' and '1mo'

    Example: 
        from app.db.session import SessionLocal // update according to the current position
        from datetime import datetime

        db = SessionLocal()
        item = {'date': '2020-01-02T00:00:00.000Z', 'open': 73.1920046399, 'high': 74.2692336173, 'low': 72.9325841905, 'close': 74.2074661255, 'volume': 135480400, 'dividends': 0, 'stock_splits': 0}
        item.date = datetime.fromisoformat(item['date'][:-1] + '+00:00').date()

        history = create_history(db, item, '1d')
    """
    ticker_table = get_ticker_table(interval)
    data = ticker_table(**history)
    db.add(data)
    db.commit()
    return data

def get_history_count(db: Session, symbol: String, start: String, end: String, interval: String):
    """
    Get number of history between start to end date in the db. 
    :param db, start, end, interval: same as get_history

    Example:
        from app.db.session import SessionLocal // update according to the current position
        db = SessionLocal()
        start = '2020-01-01'
        end = '2020-01-31'
        history = get_history_count(db, 'aapl', start, end, '1d')
    
    !IMPORTANT
        start, end date format must be 'YYYY-MM-DD'
    """
    ticker_table = get_ticker_table(interval)
    count = db.query(ticker_table).filter(ticker_table.date > start, ticker_table.date < end, ticker_table.symbol == symbol).count()
    return count