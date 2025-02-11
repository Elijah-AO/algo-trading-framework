from abc import ABC, abstractmethod

from alpaca.trading.client import TradingClient

from exchange.alpaca.latest import AlpacaLatestClient
from strategy.helpers import Instrument, Signal


class Executor(ABC):
    def __init__(
        self, trading_client: TradingClient, latest_client: AlpacaLatestClient
    ) -> None:
        self.trading_client = trading_client
        self.latest_client = latest_client

    @abstractmethod
    def submit_order(self, signal: Signal, instrument: Instrument):
        pass
