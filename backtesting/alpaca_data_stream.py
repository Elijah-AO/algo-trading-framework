from typing import Optional
from backtesting.market_data_stream import MarketDataStream
from exchange.alpaca.helpers import MarketDataType, MarketEventType
from exchange.historical_client import HistoricalClient
from datetime import datetime

from alpaca.data.timeframe import TimeFrame

from strategy.helpers import Instrument
from strategy.strategy import Strategy
from time import sleep


class AlpacaDataStream(MarketDataStream):
    def __init__(
        self, historical_client: HistoricalClient, strategy: Strategy, delay: float = 0
    ) -> None:
        super().__init__(historical_client, strategy, delay)

    def load_data(
        self,
        market_data_type: MarketDataType,
        market_event_type: MarketEventType,
        symbol: str,
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
        limit: Optional[int] = None,
    ) -> None:
        data = self.historical_client.get_historical_data(
            market_data_type,
            market_event_type,
            [symbol],
            timeframe,
            start,
            end,
            limit=limit,
        )[symbol]

        for d in data:
            self.stream.append(d)

        sleep(self.delay)
        print(f"{len(self.stream)} {market_event_type.value}s loaded for {symbol}\n")

    def start_stream(self) -> None:
        while self.stream:
            self.strategy.on_market_data(self.stream.popleft())
            sleep(self.delay)
