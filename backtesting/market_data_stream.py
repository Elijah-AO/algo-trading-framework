from abc import ABC, abstractmethod
from datetime import datetime

from alpaca.data.timeframe import TimeFrame
from collections import deque

from exchange.alpaca.helpers import MarketDataType, MarketEventType
from exchange.historical_client import HistoricalClient
from strategy.helpers import Instrument
from strategy.strategy import Strategy


# TODO: Enable multiple data streaming
# TODO: Change load data to use data from db
class MarketDataStream(ABC):
    def __init__(
        self, historical_client: HistoricalClient, strategy: Strategy, delay: float
    ) -> None:
        self.historical_client = historical_client
        self.strategy = strategy
        self.delay = delay
        self.stream = deque()

    @abstractmethod
    def load_data(
        self,
        market_data_type: MarketDataType,
        market_event_type: MarketEventType,
        symbol: str,
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
        limit: int,
    ) -> None:
        pass

    @abstractmethod
    def start_stream(self) -> None:
        pass
