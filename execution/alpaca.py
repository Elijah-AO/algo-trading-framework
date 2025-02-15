from typing import Tuple
from alpaca.trading.requests import MarketOrderRequest
from exchange.alpaca.helpers import MarketEventType
from exchange.alpaca.latest import AlpacaLatestClient
from execution.executor import Executor
from alpaca.trading.client import TradingClient
from strategy.helpers import Signal, Instrument
from alpaca.trading.enums import OrderType, OrderSide, TimeInForce


class AlpacaExecutor(Executor):
    def __init__(
        self,
        trading_client: TradingClient,
        latest_client: AlpacaLatestClient,
    ):
        super().__init__(trading_client, latest_client)

    def submit_order(
        self, signal: Signal, instrument: Instrument, signal_price: float
    ) -> None:
        """Executes an order based on signal and available balance."""
        print("submitting order")

        price, quantity = self.get_trade_size(instrument)
        if quantity <= 0:
            print(f"Skipping order: Not enough balance for {instrument.symbol}")
            return

        # TODO: Choose order type based on factors e.g volatility, spread etc

        side = OrderSide.BUY if signal == Signal.BUY else OrderSide.SELL

        try:
            print(
                f"Submitting {side.value} order for {quantity} shares of {instrument.symbol} at ${price}"
            )
            print(
                self.trading_client.submit_order(
                    MarketOrderRequest(
                        **{
                            "qty": quantity,
                            "symbol": instrument.symbol,
                            "side": side,
                            "time_in_force": TimeInForce.GTC,
                        }
                    )
                )
            )
        except Exception as e:
            print(f"Order failed: {e}")

    # TODO: Improve logic
    def get_trade_size(self, instrument: Instrument) -> Tuple[float, float]:
        account = self.trading_client.get_account()
        for a in account:
            print(a)
        buying_power = float(account.non_marginable_buying_power)

        price = self.latest_client.get_latest_data(
            instrument.market_data_type, MarketEventType.TRADE, [instrument.symbol]
        )[instrument.symbol].price

        if price == 0:
            return 0, 0

        max_shares = float(buying_power / price) * 0.95
        return (price, max_shares) if max_shares > 0 else (0, 0)
