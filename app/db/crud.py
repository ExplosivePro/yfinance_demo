from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas


def get_history(db: Session, start: Date, end: Date):
    history = db.query(models.TickerHistory).filter(models.TickerHistory.date >= start AND models.TickerHistory.date <= end).all()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

def create_history(db: Session, history):
    data = models.TickerHistory(history)
    db.add(data)
    db.commit()
    return data

def get_history_count(db: Session, start: Date, end: Date):
    count = db.query(models.TickerHistory).filter(models.TickerHistory.date >= start AND models.TickerHistory.date <= end).count()
    return count