import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # NEW
from stock import Stock
import uvicorn
from datetime import datetime

app = FastAPI()

# NEW
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ticker = Stock('aapl')

@app.get("/api/")
def get_stock_data(ticker_symbol, start, end, interval):
    ticker.ticker_symbol = ticker_symbol
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start, date_format)
    end = datetime.strptime(end, date_format)

    result = ticker.getHistory(start, end, interval)
    if not result:
        return {'error': '%s information is not found' %ticker_symbol}
    else:
        return result
        


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)