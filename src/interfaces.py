from abc import ABC, abstractmethod
from typing import List
import numpy as np
import pandas as pd 

class PricesSource:
    @abstractmethod
    def get_price(self, start_date: str, end_date: str, symbols: List[str]) -> pd.DataFrame:
        pass

class RiskModel:
    @abstractmethod
    def covariance(self, prices: pd.DataFrame) -> pd.DataFrame:
        pass

class SignalModel:
    @abstractmethod
    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        pass

class Optimizer:
    @abstractmethod
    def optimize(self, signal: pd.Series, cov: pd.DataFrame) -> pd.Series:
        pass


