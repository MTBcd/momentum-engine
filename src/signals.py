import numpy as np
import pandas as pd
from .interfaces import SignalModel
from .config import BacktestConfig
from typing import List

class MomentumSignal(BacktestConfig):
    def __init__(self, config: BacktestConfig):
        self.config = config

    def compute(self, prices: pd.DataFrame) -> pd.Series:
        lookback = self.config.lookback_window
        momentum = (
            prices.shift(self.config.skip_days) / prices.shift(self.lookback_window) - 1
        )

        return self._zscrore(momentum)

    @staticmethod
    def _zscore(self, prices: pd.DataFrame) -> pd.Series:
        mean = prices.mean(axis=1)
        std = prices.std(axis=1, ddof=1)

        return prices.sub(mean, axis=0).div(std, axis=0)