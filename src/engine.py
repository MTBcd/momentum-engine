import pandas as pd
import numpy as np
from .config import BacktestConfig
from dataclasses import dataclass
from .interfaces import Optimizer, RiskModel, SignalModel, PricesSource

@dataclass
class BacktestEngine:
    config : BacktestConfig
    price_source : PricesSource
    signal_model : SignalModel
    risk_model : RiskModel
    optimizer : Optimizer

    def run(self) -> pd.Series:
        prices = self.price_source.get_price(
            start_date = self.config.star_date,
            end_date = self.config.end_date,
            symbols = self.config.univers,
        )

        self._validate_prices(prices)

        returns = prices.pct_change()
        signal = self.signal_model.compute(prices)
        latest_signal = signal.dropna().iloc[-1]
        cov = self.risk_model.covariance(returns)

        weights = self.optimizer.optimize(signal=latest_signal, cov=cov)

        return weights

    @staticmethod
    def _validate_prices(self, prices: pd.DataFrame) -> pd.DataFrame:
        if not prices.index.is_monotonic_increasing:
            raise ValueError("The dates are not sorted")

        if prices.empty:
            raise ValueError("The prices dataframe is empty")

        if (prices < 0).any().any():
            raise ValueError("The prices can't be negative")
        
        if prices.isnull().mean().max() > 0.05:
            raise ValueError("There are too many missing values")
        

        




    






