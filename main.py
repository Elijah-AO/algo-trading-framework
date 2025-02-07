from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from dotenv import load_dotenv
import os

from exchange.alpaca.historical import AlpacaHistoricalClient
from exchange.alpaca.helpers import MarketDataType, MarketEventType


def main():
    # initialise components
    load_dotenv()

    # no keys required for crypto data
    api_key = os.getenv("APCA_API_KEY_ID") or ""
    api_secret = os.getenv("APCA_API_SECRET_KEY") or ""
    client = AlpacaHistoricalClient(api_key, api_secret)
    symbols = ["AAPL241220C00300000"]
    symbols = ["AAPL"]
    symbols = ["BTC/USD", "ETH/USD"]

    df = client.get_historical_data(
        MarketDataType.CRYPTO,
        MarketEventType.TRADE,
        symbols,
        TimeFrame.Day,
        datetime(2022, 7, 1),
        datetime(2022, 7, 4),
    )
    print(df.head())


if __name__ == "__main__":
    main()
