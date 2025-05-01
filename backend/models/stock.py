from pydantic import BaseModel

class Stock(BaseModel):
    stock_name: str
    ticker_code: str
