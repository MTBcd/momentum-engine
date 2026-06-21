import pandas as pd
import yfinance as yf
from typing import List
from .interfaces import PriceSource
from concurrent.futures import ThreadPoolExecutor, as_completed


class YahooPriceSource(PriceSource):
    def get_price_ticker(self, start: str, end: str, symbols: List[str]) -> pd.DataFrame:
        df = yf.download(tickers=symbols, 
                             start=start, 
                             end=end, 
                             auto_adjust=True,
                             threads=False,)
    
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

    def download_price(self, 
                       tickers: str, 
                       start: str, 
                       end: str, 
                       max_workers: int=8) -> pd.DataFrame:
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.get_price_ticker, ticker, start, end): ticker
                for ticker in tickers
            }

            for future in as_completed(futures):
                ticker = futures[future]

                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    print(f"Failed to download {ticker}: {e}")

        if not results:
            raise ValueError("No price data downloaded")

        prices = pd.concat(results, axis=1)
        prices = prices.sort_index()
        prices = prices[tickers]  # preserve original ticker order

        return prices







