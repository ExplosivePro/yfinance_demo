#!/usr/bin/env python3

from app.db.session import get_db
from app.db.crud import create_history
from app.db.models import TickerHistory
from app.db.session import SessionLocal, engine
from sqlalchemy import MetaData, Date, Table, Column, String, Float, BigInteger, Integer
from datetime import datetime

def init() -> None:
    db = SessionLocal()
    task = [
        {'date': '2020-01-02T00:00:00.000Z', 'symbol':'apple', 'open': 73.1920046399, 'high': 74.2692336173, 'low': 72.9325841905, 'close': 74.2074661255, 'volume': 135480400, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-02T00:00:00.000Z', 'symbol':'google', 'open': 73.1920046399, 'high': 74.2692336173, 'low': 72.9325841905, 'close': 74.2074661255, 'volume': 135480400, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-03T00:00:00.000Z', 'symbol':'apple', 'open': 73.4168436558, 'high': 74.2642918847, 'low': 73.2562496755, 'close': 73.4860229492, 'volume': 146322800, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-06T00:00:00.000Z', 'symbol':'apple', 'open': 72.586693487, 'high': 74.1111110822, 'low': 72.3297385897, 'close': 74.0715789795, 'volume': 118387200, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-07T00:00:00.000Z', 'symbol':'apple', 'open': 74.0814601343, 'high': 74.3433537036, 'low': 73.4983786146, 'close': 73.7232131958, 'volume': 108872000, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-08T00:00:00.000Z', 'symbol':'apple', 'open': 73.4193174657, 'high': 75.2179866504, 'low': 73.4193174657, 'close': 74.9091491699, 'volume': 132079200, 'dividends': 0, 'stock_splits': 0},
        {'date': '2020-01-09T00:00:00.000Z', 'symbol':'apple', 'open': 75.9097738212, 'high': 76.6979276147, 'low': 75.6528264858, 'close': 76.5002746582, 'volume': 170108400, 'dividends': 0, 'stock_splits': 0}
    ]
    if not engine.dialect.has_table(engine.connect(), 'stock_history_1d'):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table('stock_history_1d', metadata,
            Column('date', Date, primary_key=True, index=True), 
            Column('symbol', String, primary_key=True),
            Column('open', Float),Column('high', Float),
            Column('low', Float),Column('close', Float),
            Column('volume', BigInteger),Column('stock_splits', Integer),
            Column('dividends', Integer)
        )
        # Implement the creation
        metadata.create_all()
    try:
        for item in task:
            item['date'] = datetime.fromisoformat(item['date'][:-1] + '+00:00').date()
            create_history(db, item, '1d')
    finally:
        return


if __name__ == "__main__":
    init()
