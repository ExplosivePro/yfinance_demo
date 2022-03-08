from distutils.log import error
import yfinance as yf
import json
from app.db.session import SessionLocal, engine
from app.db.crud import get_history_count, get_history
from sqlalchemy import Date, String
from datetime import datetime
from dateutil import rrule

class Stock:
    """
        Basic Usage
        ticker = Stock("aapl")
        result = ticker.getHistory("2020-01-02", "2020-01-10")

        ticker.ticker_symbol = "aapl"
        result = ticker.getHistory("2020-01-02", "2020-01-10", "1wk")
    """
    
    def __init__(self, ticker_symbol):
        # initialize ticker with ticker_symbol, db setting
        self.ticker = yf.Ticker(ticker_symbol)
        self._ticker_symbol = ticker_symbol
        self._tbl_name = '%s_table' %ticker_symbol
        self._db = SessionLocal()

    def getHistory(self, start: Date, end: Date, interval='1d'):
        '''
            Get stock history information from db or yahoo finance and save it to db.

            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1wk and 1mo

            :return stock history information in JSON
        '''
        try:
            if self._existInDB(start, end, interval):
                # get existing parts
                result = self._getHistoryFromDB(start, end, interval)
                chunks = self._getMissingChunks(start, end, interval)
                # get missing parts from API and merge it to the result
                for chunk in chunks:
                    missing = self._getHistory(start=chunk['start'], end=chunk['end'], interval=interval)
                    if self.result.empty is False:
                        self._save2DB(interval)
                    json_result = missing.to_json(orient="table")
                    parsed = json.loads(json_result)
                    result += parsed
                return result
        finally:
            # Get stock information using yahoo finance api
            self._getHistory(start, end, interval)

            # if result is not empty, save to database
            if self.result.empty is False:
                self._save2DB(interval)

            # Convert Result to JSON object 
            json_result = self.result.to_json(orient="table")
            parsed = json.loads(json_result)
            return parsed
    
    def _existInDB(self, start:Date, end:Date, interval: String):
        '''
            Check same search was already conducted before
            Compare the size of the data in the database satisifying the condition and the expected search result size
            
            :param start: date from which start search
            :param end: date to which start search
            :param interval: search intensity, can be one of 1d, 1wk and 1mo

            :return True if whole data exists in DB, False otherwise
        '''
        try:
            # Count of items that is searched already
            # Calculate expected searh result size
            delta = end - start
            expected_count = rrule.rrule(rule.DAILY, dtstart=star, until=end).count() - 2:
            unit = rule.DAILY
            if interval == '1wk':
                unit = rule.WEEKLY
            elif interval == '1mo':
                expected_count = rule.MONTHLY
            return count == expected_count
        except Exception:
            return False
        
    def _getHistoryFromDB(self, start: Date, end: Date, interval: String):
        '''
            Get the previous search result stored in database

            :param start: date from which start search
            :param end: date to which start search
            :param interval: search intensity, can be one of 1d, 1wk and 1mo

            :return True if whole data exists in DB, False otherwise
        '''
        result = get_history(self._db, symbol=self._ticker_symbol,start=start, end=end, interval=interval)

        return [r.as_dict() for r in result]

    def _getMissingChunks(self, start: Date, end: Date, interval: String):
        '''
            Get Missing Date Ranges that need to be merged to the data of database
            :param start: date from which start search
            :param end: date to which start search
            :param interval: search intensity, can be one of 1d, 1wk and 1mo

            :return list of missing chunks in the following format 
                [{start: ..., end: ...}, {start: ..., end: ...}]
        '''
        existing = self._getHistoryFromDB(start=start, end=end, interval=interval)
        unit = rrule.DAILY
        if interval == '1wk':
            unit = rrule.WEEKLY
        elif interval == '1mo':
            unit = rrule.MONTHLY

        missing = []
        
        date_format = "%Y-%m-%d"
        prev = datetime.strptime(start, date_format).date()

        for item in existing:
            if rrule.rrule(unit, dtstart=item['date'], until=prev).count() > 2:
                missing.append({'start': prev, 'end': item['date']})
            prev = item['date']

        return missing

    def _getHistory(self, start: Date, end: Date, interval: String):
        '''
            Get stock history information from yahoo finance
            
            :param start_date: date from which start search
            :param end_date: date to which start search
            :param interval: search intensity, can be one of 1d, 1wk and 1mo

            :return search result in pandas.DateFrame
        '''
        if type(start) == str:
            start_date = start
        else:
            start_date = start.strftime("%Y-%m-%d")
        if type(end) == str:
            end_date = end
        else:
            end_date = end.strftime("%Y-%m-%d")
        result = self.ticker.history( symbol=self.ticker_symbol ,start=start_date, end=end_date, interval=interval)
        self.result = result
        return result

    def _save2DB(self, interval:String):
        '''
            Save Result that was gained using yfinance to database
            
            :param interval: Search Interval, one of '1d', '1wk', '1mo'
            :return void

            !IMPORTANT
                Should be called after _getHistory function
        '''
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
            dtype={'date': Date}, index_label='date',
            con=engine.connect(), if_exists='append', index = True
        )

    @property
    def ticker_symbol(self):
        return self._ticker_symbol

    @ticker_symbol.setter
    def ticker_symbol(self, value: String):
        self._ticker_symbol = value
        self.ticker = yf.Ticker(value)
