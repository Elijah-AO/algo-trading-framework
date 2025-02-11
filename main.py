from alpaca.data.requests import CorporateActionsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.models import TradeAccount
from dotenv import load_dotenv
import os
from typing import List

from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from exchange.alpaca.historical import AlpacaHistoricalClient
from exchange.alpaca.helpers import MarketDataType, MarketEventType
from exchange.alpaca.live import AlpacaLiveClient
from exchange.alpaca.latest import AlpacaLatestClient
from execution.alpaca import AlpacaExecutor
from strategy.helpers import Instrument, Signal
from strategy.sma import SMA
from strategy.strategy import Strategy


def main():
    # initialise components
    load_dotenv()

    # no keys required for crypto data
    api_key = os.getenv("APCA_API_KEY_ID") or ""
    api_secret = os.getenv("APCA_API_SECRET_KEY") or ""
    auth = api_key, api_secret

    market_data_type = MarketDataType.CRYPTO
    event_type = MarketEventType.QUOTE
    timeframe = TimeFrame.Day
    start = datetime(2022, 7, 1)
    end = datetime(2022, 7, 7)

    symbols = ["AAPL241220C00300000"]
    symbols = ["AAPL"]
    symbols = ["*"]
    symbols = ["ETH/USD"]
    symbols = ["AAPL", "TSLA", "NVDA"]
    symbols = ["NVDA"]
    symbols = ["BTC/USD"]
    #
    # df = client.get_latest_data(
    #     MarketDataType.STOCK,
    #     MarketEventType.SNAPSHOT,
    #     symbols,
    #     TimeFrame.Day,
    #     start,
    #     end,
    # )
    #
    # print(df)
    #

    """
    Example control flow:
    initialise live (for websocket streaming)
    initialise latest client (for snapshots)
    initialise strategy
    initialise executor

    live client streams data to strategy
    strategy generates signals
    submits orders with executor

    executor uses latest client to get snapshot and decide order type 
    checks our account to see if we can buy/sell the stock (do we have the money, is the asset tradable)
    submits order
    """

    instrument = Instrument("BTC/USD", MarketDataType.CRYPTO)
    latest_client = AlpacaLatestClient(*auth)
    live_client = AlpacaLiveClient(*auth)
    trading_client = TradingClient(*auth)
    executor = AlpacaExecutor(trading_client, latest_client)
    strategy_1 = SMA(executor, 1, 2, instrument)
    strategies: List[Strategy]
    strategies = [strategy_1]
    # print(latest_client.get_latest_data(market_data_type, event_type, symbols))

    # live_client.subscribe_symbols(market_data_type, MarketEventType.QUOTE, symbols)
    # live_client.subscribe_symbols(market_data_type, MarketEventType.TRADE, symbols)
    # live_client.subscribe_symbols(market_data_type, MarketEventType.BAR, symbols)
    # live_client.subscribe_strategies(strategies)
    # live_client.start_stream(market_data_type)
    print(executor.submit_order(Signal.BUY, instrument))


if __name__ == "__main__":
    main()
