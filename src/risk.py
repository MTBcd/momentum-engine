from .interfaces import RiskModel
import pandas as pd
import numpy as np

class SampleCovariance(RiskModel):
    def linear_cov(self, returns: pd.DataFrame) -> pd.DataFrame:
        cov = returns.dropna().cov() 

        if cov.isnull().any().any():
            raise ValueError("Covariance matrix contain NaNs")
        
        return cov
    

