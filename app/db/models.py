from sqlalchemy import Column, Integer, Date, Float, BigInteger,String
from sqlalchemy.ext.declarative import declarative_base

def get_ticker_table(interval):
    DynamicBase = declarative_base(class_registry=dict())
    class TickerHistory(DynamicBase):
        __tablename__ = 'stock_history_%s' %(interval)
        date = Column(Date, primary_key=True, index=True)
        symbol = Column(String, primary_key=True)
        open = Column(Float)
        high = Column(Float)
        low = Column(Float)
        close = Column(Float)
        volume = Column(BigInteger)
        stock_splits = Column(Integer)
        dividends = Column(Integer)
        def as_dict(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    return TickerHistory


