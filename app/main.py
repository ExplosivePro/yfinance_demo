from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # NEW
from stock import Stock
import uvicorn

app = FastAPI()

# NEW
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ticker = Stock('aapl')

@app.get("/api/")
def get_stock_data(ticker_symbol, start, end, interval):
    ticker.ticker_symbol = ticker_symbol
    result = ticker.getHistory(start, end, interval)

    if not result:
        return result
    else:
        return {'error': '%s information is not found' %ticker_symbol}
        


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)