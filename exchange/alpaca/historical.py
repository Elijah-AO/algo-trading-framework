from alpaca.data.historical import (
    CryptoHistoricalDataClient,
    OptionHistoricalDataClient,
    StockHistoricalDataClient,
    NewsClient,
)
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from pandas import DataFrame
from exchange.alpaca.helpers import (
    MarketDataType,
    MarketEventType,
    HISTORICAL_REQUEST_CLASSES,
    HISTORICAL_CLIENT_MAPPING,
    REQUEST_LIMIT,
)


class AlpacaHistoricalClient:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.stock_client = StockHistoricalDataClient(api_key, api_secret)
        self.crypto_client = CryptoHistoricalDataClient(api_key, api_secret)
        self.option_client = OptionHistoricalDataClient(api_key, api_secret)
        self.news_client = NewsClient(api_key, api_secret)

    def get_historical_data(
        self,
        market_data_type: MarketDataType,
        event_type: MarketEventType,
        symbols: list[str],
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
    ) -> DataFrame:
        if market_data_type not in HISTORICAL_REQUEST_CLASSES:
            raise NotImplementedError(
                f"Market data type '{market_data_type.value}' is not supported."
            )

        if event_type not in HISTORICAL_REQUEST_CLASSES[market_data_type]:
            raise NotImplementedError(
                f"'{event_type.value}' data is not available for {market_data_type.value}."
            )

        request_class = HISTORICAL_REQUEST_CLASSES[market_data_type][event_type]

        request_params = request_class(
            symbol_or_symbols=symbols,
            timeframe=timeframe if timeframe else None,
            limit=REQUEST_LIMIT,
            start=start,
            end=end,
        )

        if (
            event_type == MarketEventType.NEWS
            and market_data_type == MarketDataType.NEWS
        ):
            request_params.limit = 50
            return self.news_client.get_news(request_params).df

        client_attr = HISTORICAL_CLIENT_MAPPING[market_data_type]
        client = getattr(self, client_attr)

        method_name = f"get_{market_data_type.value}_{event_type.value}s"

        if not hasattr(client, method_name):
            raise NotImplementedError(
                f"{client_attr} does not support {event_type.value} data."
            )

        method = getattr(client, method_name)

        bars = method(request_params)

        return bars.df
