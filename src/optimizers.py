from scipy import optimize
import pandas as pd
import numpy as np 
from .interfaces import Optimizer

class LongOnlyTopNOptimizer(Optimizer):
    def __init__(self, n_names: str, max_weights: float):
        self.n_names = n_names
        self.max_weights = max_weights

    def optimize(self, signal: pd.Series, cov: pd.DataFrame) -> pd.Series:
        signal = signal.dropna()
        common = signal.index.intersection(cov.index)
        cov = cov.loc[common]
        signal = signal.loc[common]

        selected = signal.nlargest(self.n_names).index
        
        weights = pd.Series(0.0, index=cov.index)
        raw_weights = min(1 / len(selected), self.max_weights)
        weights.loc[selected] = raw_weights
        weights = weights / weights.sum()

        if not np.isclose(weights.sum(), 1.0):
            raise ValueError("weights does not sum to one")

        return weights
    
