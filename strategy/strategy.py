from abc import ABC, abstractmethod
from alpaca.trading.enums import OrderType
from execution.executor import Executor
from strategy.helpers import Signal


class Strategy(ABC):
    def __init__(self, executor: Executor) -> None:
        self.executor = executor

    @abstractmethod
    def on_market_data(self, data):  # TODO: Add type
        pass

    @abstractmethod
    def send_order(self, signal: Signal, signal_price: float):
        pass
