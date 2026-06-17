import pandas as pd
import yfinance as yf
from typing import List
from .interfaces import PriceSource


class YahooPriceSource(PriceSource):
    def get_prices(self, start: str, end: str, symbols: List[str]) -> pd.DataFrame:
        df = yf.download(tickers=symbols, 
                             start=start, 
                             end=end, 
                             auto_adjust=True)
        
        if df.empty :
            raise ValueError("Yahoo return an empty dataframe")
        
        if isinstance(df.columns, pd.MultiIndex):
            prices = df["close"]
        else:
            prices = df[["close"]].rename(columns={"Close": symbols[0]})
        
        prices = prices.sort_index()

        if prices.empty:
            raise ValueError("No prices available")
        
        return prices




