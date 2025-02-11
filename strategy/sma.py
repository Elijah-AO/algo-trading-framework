from typing import Optional, Union
import numpy as np
import pandas as pd
from execution.executor import Executor
from strategy.helpers import Instrument, Signal
from strategy.strategy import Strategy  # TODO: change this
from collections import deque
from typing import Dict
from alpaca.data.models import Bar, Quote, Trade


class SMA(Strategy):
    def __init__(
        self,
        executor: Executor,
        short_period: int,
        long_period: int,
        instrument: Instrument,
    ) -> None:
        super().__init__(executor)
        self.short_sma = deque(maxlen=short_period)
        self.long_sma = deque(maxlen=long_period)
        self.short_period = short_period
        self.long_period = long_period
        self.instrument = instrument

    def calculate_sma(self, deque_window: deque) -> float:
        return sum(deque_window) / len(deque_window) if deque_window else 0

    def on_market_data(self, data: Bar) -> None:
        print(f"DATA: {data}")

        self.short_sma.append(data.close)
        self.long_sma.append(data.close)

        short_mean = self.calculate_sma(self.short_sma)
        long_mean = self.calculate_sma(self.long_sma)

        print(f"Long SMA: {long_mean}, Short SMA: {short_mean}")

        if len(self.long_sma) < self.long_period:
            return

        if short_mean > long_mean:
            self.send_order(Signal.BUY)
        elif short_mean < long_mean:
            self.send_order(Signal.SELL)

    def send_order(self, signal: Signal) -> None:
        return self.executor.submit_order(signal, self.instrument)
