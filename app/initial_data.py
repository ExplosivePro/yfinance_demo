#!/usr/bin/env python3

from app.db.session import get_db
from app.db.crud import create_history
from app.db.models import TickerHistory
from app.db.session import SessionLocal
from datetime import datetime


def init() -> None:
    db = SessionLocal()
    
    task = [{'date': '2020-01-02T00:00:00.000Z', 'open': 73.1920046399, 'high': 74.2692336173, 'low': 72.9325841905, 'close': 74.2074661255, 'volume': 135480400, 'dividends': 0, 'stock_splits': 0}, {'date': '2020-01-03T00:00:00.000Z', 'open': 73.4168436558, 'high': 74.2642918847, 'low': 73.2562496755, 'close': 73.4860229492, 'volume': 146322800, 'dividends': 0, 'stock_splits': 0}, {'date': '2020-01-06T00:00:00.000Z', 'open': 72.586693487, 'high': 74.1111110822, 'low': 72.3297385897, 'close': 74.0715789795, 'volume': 118387200, 'dividends': 0, 'stock_splits': 0}, {'date': '2020-01-07T00:00:00.000Z', 'open': 74.0814601343, 'high': 74.3433537036, 'low': 73.4983786146, 'close': 73.7232131958, 'volume': 108872000, 'dividends': 0, 'stock_splits': 0}, {'date': '2020-01-08T00:00:00.000Z', 'open': 73.4193174657, 'high': 75.2179866504, 'low': 73.4193174657, 'close': 74.9091491699, 'volume': 132079200, 'dividends': 0, 'stock_splits': 0}, {'date': '2020-01-09T00:00:00.000Z', 'open': 75.9097738212, 'high': 76.6979276147, 'low': 75.6528264858, 'close': 76.5002746582, 'volume': 170108400, 'dividends': 0, 'stock_splits': 0}]
    for item in task:
        item['date'] = datetime.fromisoformat(item['date'][:-1] + '+00:00').date()
        create_history(db, item)


if __name__ == "__main__":
    init()
