import yfinance as yf
import json
from app.db.session import SessionLocal
from app.db.crud import get_history_count
from datetime import datetime

class Stock:
    """
        Basic Usage
        ticker = Stock("aapl")
        result = ticker.getHistory("2020-01-02", "2020-01-10")

        ticker.ticker_symbol = "aapl"
        result = ticker.getHistory("2020-01-02", "2020-01-10", "1w")
    """
    
    def __init__(self, ticker_symbol):
        # initialize tiker with ticker_symbol, db setting
        self.ticker = yf.Ticker(ticker_symbol)
        self._ticker_symbol = ticker_symbol
        self._tbl_name = '%s_table' %ticker_symbol 

    def getHistory(self, start_date, end_date, interval='1d'):
        '''
            Get stock history information from db or yahoo finance and save it to db.

            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1w and 1m

            :return stock history information in JSON
        '''

        # If searched already, get from database
        if self._existInDB(start_date, end_date, interval):
            return self._getHistoryFromDB(self, start_date, end_date)

        # Get stock information using yahoo finance api
        self._getHistory(start_date, end_date, interval)

        # if result is not empty, save to database
        if self.result.empty is False:
            self._save2DB(interval)

        # Convert Result to JSON object 
        json_result = self.result.to_json(orient="table")
        parsed = json.loads(json_result)
        return parsed
    
    def _existInDB(self, start_date, end_date, interval):
        '''
            Check same search was already conducted before
            Compare the size of the data in the database satisifying the condition and the expected search result size
            
            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1w and 1m

            :return True if whole data exists in DB, False otherwise
        '''
        db = SessionLocal()
        try:
            # Count of items that is searched already
            count = get_history_count(db, self.ticker_symbol ,start_date, end_date, interval)
            
            # Calculate expected searh result size
            date_format = "%m/%d/%Y"
            start = datetime.strptime(start_date, date_format)
            end = datetime.strptime(end_date, date_format)
            delta = end - start
            expected_count = delta.days

            if interval == '1w':
                expected_count = delta.weeks
            elif interval == '1m':
                expected_count = delta.month

            return count == expected_count
        finally:
            return False
        
    def _getHistoryFromDB(self, start_date, end_date, interval):
        '''
            Get the previous search result stored in database

            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1w and 1m

            :return True if whole data exists in DB, False otherwise
        '''
        db = SessionLocal()
        return get_history_count(db, self.ticker_symbol ,start_date, end_date, interval)

    def _getHistory(self, start_date, end_date, interval):
        '''
            Get stock history information from yahoo finance
            
            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1w and 1m
        '''
        self.result = self.ticker.history(start=start_date, end=end_date, interval=interval)

    def _save2DB(self, interval):
        '''
            Save Result that was gained using yfinance to database
            
            :param interval: Search Interval, one of '1d', '1w', '1m'
            :return void

            !IMPORTANT
                Should be called after _getHistory function
        '''
        db = SessionLocal()
        columns={
            "Date": "date",
            "Stock Splits": "stock_splits",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
            "Dividends": "dividends"
        }
        self.result.rename(columns=columns, inplace = True)
        self.result = self.result.assign(symbol=self._ticker_symbol)
        # self.result.head(5)
        self.result.to_sql(
            'stock_history_%s' %(interval), 
            dtype={'date': 'DATE PRIMARY KEY'}, index_label='date',
            con=db.connect(), if_exists='append', index = True
        )

    @property
    def ticker_symbol(self):
        return self._ticker_symbol

    @ticker_symbol.setter
    def ticker_symbol(self, value):
        self._ticker_symbol = value
        self.ticker = yf.Ticker(value)
