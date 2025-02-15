from abc import ABC, abstractmethod
from typing import Optional
from pandas import DataFrame
from datetime import datetime

from exchange.alpaca.helpers import MarketDataType, MarketEventType
from alpaca.data import TimeFrame


# TODO: Generalise marketdatyatype and event type enums
class HistoricalClient(ABC):
    @abstractmethod
    def get_historical_data(
        self,
        market_data_type: MarketDataType,
        market_event_type: MarketEventType,
        symbols: list[str],
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
        limit: Optional[int] = None,
    ) -> DataFrame:
        pass
