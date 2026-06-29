from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class BacktestConfig:
    start_date: str
    end_date: str
    univers: list[str]
    lookback_window: int = 252
    skip_days: int = 21
    n_names: int = 5
    max_weight: float = 0.25
    data_snapshot_id: str = "yahoo_research"



