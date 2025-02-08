from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from dotenv import load_dotenv
import os

from exchange.alpaca.historical import AlpacaHistoricalClient
from exchange.alpaca.helpers import MarketDataType, MarketEventType
from exchange.alpaca.live import AlpacaLiveClient


def main():
    # initialise components
    load_dotenv()

    # no keys required for crypto data
    api_key = os.getenv("APCA_API_KEY_ID") or ""
    api_secret = os.getenv("APCA_API_SECRET_KEY") or ""
    client = AlpacaHistoricalClient(api_key, api_secret)

    market_data_type = MarketDataType.CRYPTO
    event_type = MarketEventType.BAR
    timeframe = TimeFrame.Day
    start = datetime(2022, 7, 1)
    end = datetime(2022, 7, 7)

    symbols = ["AAPL241220C00300000"]
    symbols = ["BTC/USD", "ETH/USD"]
    symbols = ["AAPL"]
    symbols = ["*"]
    symbols = ["AAPL"]

    df = client.get_historical_data(
        MarketDataType.STOCK,
        MarketEventType.BAR,
        symbols,
        TimeFrame.Day,
        datetime(2022, 7, 1),
        datetime(2022, 7, 7),
    )

    print(df.head())

    client = AlpacaLiveClient(api_key, api_secret)
    client.subscribe(market_data_type, event_type, symbols)
    client.start_stream(market_data_type)


if __name__ == "__main__":
    main()
