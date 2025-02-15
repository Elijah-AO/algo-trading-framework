from typing import Dict
from execution.executor import Executor
from strategy.helpers import Signal, Instrument
from datetime import datetime
from collections import defaultdict


class MockExecutor(Executor):
    def __init__(self, trading_client, latest_client):
        super().__init__(trading_client, latest_client)
        self.trades = []
        self.pnl = 0.0
        self.positions: defaultdict[str, int] = defaultdict(int)

    def record_trade(self, signal: Signal, instrument: Instrument, price: float):
        trade = {
            "signal": signal,
            "instrument": instrument,
            "price": price,
            "timestamp": datetime.now(),
        }
        symbol = instrument.symbol
        if signal == Signal.BUY:
            self.pnl -= price
            self.positions[symbol] += 1
            self.trades.append(trade)

        elif signal == Signal.SELL and self.positions[symbol]:
            self.pnl += price
            self.positions[symbol] -= 1
            self.trades.append(trade)

    def pnl_stats(self):
        sells = 0
        buys = 0
        for trade in self.trades:
            if trade["signal"] == Signal.BUY:
                buys += 1

            elif trade["signal"] == Signal.SELL:
                sells += 1
        print(f"{buys} buys, {sells} sells, total pnl: {self.pnl}")

    def submit_order(self, signal: Signal, instrument: Instrument, signal_price: float):
        self.record_trade(signal, instrument, signal_price)
        print(
            f"Mock order submitted: {signal.value} {instrument.symbol} at {signal_price}"
        )
        print(f"Current PnL: {self.pnl}")
