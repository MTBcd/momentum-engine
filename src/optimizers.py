import pandas as pd
import numpy as np 
from .interfaces import Optimizer
from functools import wraps 
import time

def timed(fn):
    @wraps(fn)
    def wrap(*a, **k):
        t0 = time.perf_counter()
        r = fn(*a, **k)
        print(f"[timed] {fn.__name__} : {time.perf_counter() - t0}s")
        return r
    return wrap


class LongOnlyTopNOptimizer(Optimizer):
    def __init__(self, n_names: str, max_weights: float):
        self.n_names = n_names
        self.max_weights = max_weights
    @timed
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
    
