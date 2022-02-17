import yfinance as yf
import sqlite3
import json

class Stock:
    """
        Basic Usage
        apple = Stock("aapl")
        result = apple.getHistory("2020-01-02", "2020-01-10")

        apple.ticker_symbol = "aapl"
        result = apple.getHistory("2020-01-02", "2020-01-10")
    """
    
    def __init__(self, ticker_symbol):
        # initialize tiker with ticker_symbol, db setting
        self.ticker = yf.Ticker(ticker_symbol)
        self._ticker_symbol = ticker_symbol
        self._tbl_name = '%s_table' %ticker_symbol 

    def getHistory(self, start_date, end_date, interval='1d'):
        if self._existInDB(start_date, end_date, interval):
            return self._getHistoryFromDB(self, start_date, end_date)

        self._getHistory(start_date, end_date, interval)

        # if result is empty(which is most likely that ticker_symbol is empty), no need to save it to db.
        if self.result.empty is False:
            self._save2DB(interval)
        
        json_result = self.result.to_json(orient="table")
        parsed = json.loads(json_result)

        return parsed
    
    def _existInDB(self, start_date, end_date, interval):
        # try:
        # tbl_name = '%s_%s_table' %(self._ticker_symbol, interval)
        # # query = 'SELECT COUNT(date) as count FROM %s WHERE date>=\'%s\' AND date<=\'%s\'' %(tbl_name, start_date, end_date)
        # query = 'SELECT COUNT(date) as count FROM %s' %(tbl_name)
        # result = cur.execute(query)
        # count, = result.fetchall()[0]
        # print("count %s" %count)
        # print(query)
        return False
        # except Exception:
        #     print("error")
        #     print("error")

        #     return False

    def _getHistoryFromDB(self, start_date, end_date, interval):
        # tbl_name = '%s_%s_table' %(self._ticker_symbol, interval)
        # query = 'SELECT * FROM %s WHERE date>=\'%s\' AND date<=\'%s\'' %(tbl_name, start_date, end_date)
        # result = cur.execute(query)
        # return result.fetchall()
        return []

    def _getHistory(self, start_date, end_date, interval):
        self.result = self.ticker.history(start=start_date, end=end_date, interval=interval)

    def _save2DB(self, interval):
        # con = sqlite3.connect(self._db)
        columns={
            "Stock Splits": "stock_splits",
            "Open": "open",
            "Date": "date",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
            "Dividends": "dividends"
        }
        # self.result.rename(columns=columns, inplace = True)
        # self.result.head(5)
        # self.result.to_sql('%s_%s_table' %(self._ticker_symbol, interval), con=con, if_exists='append', index = True)

    @property
    def ticker_symbol(self):
        return self._ticker_symbol

    @ticker_symbol.setter
    def ticker_symbol(self, value):
        self._ticker_symbol = value
        self.ticker = yf.Ticker(value)
