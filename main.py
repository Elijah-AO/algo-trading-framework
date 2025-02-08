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
    symbols = ["AAPL241220C00300000"]
    symbols = ["BTC/USD", "ETH/USD"]
    symbols = ["AAPL"]

    df = client.get_historical_data(
        MarketDataType.NEWS,
        MarketEventType.NEWS,
        symbols,
        TimeFrame.Day,
        datetime(2022, 7, 1),
        datetime(2022, 7, 4),
    )
    print(df.head())
    # client = AlpacaLiveClient(api_key, api_secret)
    # client.start_crypto_stream(symbols)


if __name__ == "__main__":
    main()
