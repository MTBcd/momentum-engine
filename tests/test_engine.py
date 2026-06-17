import pytest
from dataclasses import FrozenInstanceError
from src.config import BacktestConfig

def test_config_is_frozen():
    cfg = BacktestConfig(
        start_date="2020-01-01",
        end_date="2024-01-01",
        tickers=("AAPL", "MSFT")
    )

    with pytest.raises(FrozenInstanceError):
        cfg.max_weight = 0.9