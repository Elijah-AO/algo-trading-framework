from typing import Optional
from alpaca.data.historical import (
    CryptoHistoricalDataClient,
    OptionHistoricalDataClient,
    StockHistoricalDataClient,
    NewsClient,
)

from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from pandas import DataFrame

from exchange.alpaca.helpers import (
    MarketDataType,
    MarketEventType,
    HISTORICAL_REQUEST_CLASSES,
    CLIENT_MAPPING,
    REQUEST_LIMIT,
)
from exchange.historical_client import HistoricalClient


# TODO: Create historical client interface
class AlpacaHistoricalClient(HistoricalClient):
    def __init__(self, api_key: str, api_secret: str) -> None:
        auth = api_key, api_secret
        self.stock_client = StockHistoricalDataClient(*auth)
        self.crypto_client = CryptoHistoricalDataClient(*auth)
        self.option_client = OptionHistoricalDataClient(*auth)
        self.news_client = NewsClient(*auth)
        self.corporate_action_client = CorporateActionsClient(*auth)

    def get_historical_data(
        self,
        market_data_type: MarketDataType,
        market_event_type: MarketEventType,
        symbols: list[str],
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
        limit: Optional[int] = None,
    ) -> DataFrame:
        if market_data_type not in HISTORICAL_REQUEST_CLASSES:
            raise NotImplementedError(
                f"Market data type '{market_data_type.value}' is not supported."
            )

        if market_event_type not in HISTORICAL_REQUEST_CLASSES[market_data_type]:
            raise NotImplementedError(
                f"Historical '{market_event_type.value}' data is not available for {market_data_type.value}."
            )

        request_class = HISTORICAL_REQUEST_CLASSES[market_data_type][market_event_type]

        request_params = request_class(
            symbol_or_symbols=symbols,
            timeframe=timeframe if timeframe else None,
            limit=limit,
            start=start,
            end=end,
        )

        client_attr = CLIENT_MAPPING[market_data_type]
        client = getattr(self, client_attr)

        method_name = (
            f"get_{market_data_type.value}_{market_event_type.value}s"
            if market_data_type.value != market_event_type.value
            else f"get_{market_data_type.value}"
        )

        if not hasattr(client, method_name):
            raise NotImplementedError(
                f"{client_attr} does not support {market_event_type.value} data."
            )

        method = getattr(client, method_name)

        bars = method(request_params)

        return bars
