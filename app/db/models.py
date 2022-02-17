from sqlalchemy import Boolean, Column, Integer, String, Date, Float, BigInteger

from .session import Base

class TickerHistory(Base):
    __tablename__ = "aapl_1d"
    date = Column(Date, primary_key=True, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)
    stock_splits = Column(Integer, nullable=False)
    dividends = Column(Integer, nullable=False)