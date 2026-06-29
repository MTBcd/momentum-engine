from .config import BacktestConfig
from .engine import BacktestEngine
from .data import YahooPriceSource
from .signals import MomentumSignal
from .optimizers import LongOnlyTopNOptimizer
from .risk import SampleCovariance

config = BacktestConfig(
    start_date="2018-01-01",
    end_date="2024-12-31",
    univers=("AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM", "XOM", "UNH"),
    lookback_window=252,
    skip_days=21,
    n_names=3,
    max_weight=0.40
)

engine = BacktestEngine(
    config=config,
    price_source=YahooPriceSource,
    signal_model=MomentumSignal(config),
    risk_model=SampleCovariance,
    optimizer=LongOnlyTopNOptimizer(
        n_names=config.n_names,
        max_weights=config.max_weight

    )
)

weights = engine.run()
print(weights)