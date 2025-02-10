from alpaca.data.requests import CorporateActionsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from dotenv import load_dotenv
import os

from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from exchange.alpaca.historical import AlpacaHistoricalClient
from exchange.alpaca.helpers import MarketDataType, MarketEventType
from exchange.alpaca.live import AlpacaLiveClient
from exchange.alpaca.latest import AlpacaLatestClient


def main():
    # initialise components
    load_dotenv()

    # no keys required for crypto data
    api_key = os.getenv("APCA_API_KEY_ID") or ""
    api_secret = os.getenv("APCA_API_SECRET_KEY") or ""
    client = AlpacaLatestClient(api_key, api_secret)

    market_data_type = MarketDataType.STOCK
    event_type = MarketEventType.TRADE
    timeframe = TimeFrame.Day
    start = datetime(2022, 7, 1)
    end = datetime(2022, 7, 7)

    symbols = ["AAPL241220C00300000"]
    symbols = ["BTC/USD", "ETH/USD"]
    symbols = ["AAPL"]
    symbols = ["*"]
    symbols = ["AAPL", "TSLA", "NVDA"]

    df = client.get_latest_data(
        MarketDataType.STOCK,
        MarketEventType.SNAPSHOT,
        symbols,
        TimeFrame.Day,
        start,
        end,
    )

    print(df)

    # client = AlpacaLiveClient(api_key, api_secret)
    event_type_2 = MarketEventType.QUOTE
    client.subscribe(market_data_type, event_type, symbols)
    client.subscribe(market_data_type, event_type_2, symbols)
    client.start_stream(market_data_type)


if __name__ == "__main__":
    main()
