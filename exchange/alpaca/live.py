from alpaca.data.live import (
    CryptoDataStream,
    OptionDataStream,
    NewsDataStream,
    StockDataStream,
)

from exchange.alpaca.helpers import (
    MarketDataType,
    MarketEventType,
    CLIENT_MAPPING,
    LIVE_REQUEST_CLASSES,
)
from typing import List

from strategy.strategy import Strategy


# TODO: Create live client interface
class AlpacaLiveClient:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.crypto_client = CryptoDataStream(api_key, api_secret)
        self.option_client = OptionDataStream(api_key, api_secret)
        self.news_client = NewsDataStream(api_key, api_secret)
        self.stock_client = StockDataStream(api_key, api_secret)
        self.strategies: List[Strategy]
        self.strategies = []

    async def on_data(self, data) -> None:
        for strategy in self.strategies:
            strategy.on_market_data(data)

    def subscribe_strategies(self, strategies: List[Strategy]):
        self.strategies.extend(strategies)

    def subscribe_symbols(
        self,
        market_data_type: MarketDataType,
        market_event_type: MarketEventType,
        symbols: List[str],
    ) -> None:
        if market_data_type not in LIVE_REQUEST_CLASSES:
            raise NotImplementedError(
                f"Live '{market_data_type.value}' Market data is not supported."
            )

        if market_event_type not in LIVE_REQUEST_CLASSES[market_data_type]:
            raise NotImplementedError(
                f"Live '{market_event_type.value}' data is not available for {market_data_type.value}."
            )
        client_attr = CLIENT_MAPPING[market_data_type]
        client = getattr(self, client_attr)

        if (
            market_data_type == MarketDataType.STOCK
            and market_event_type == MarketEventType.TRADING_STATUS
        ):
            method_name = "subscribe_trading_statuses"

        elif (
            market_data_type == MarketDataType.NEWS
            and market_event_type == MarketEventType.NEWS
        ):
            method_name = "subscribe_news"

        else:
            method_name = f"subscribe_{market_event_type.value}s"

        if not hasattr(client, method_name):
            raise NotImplementedError(
                f"{client_attr} does not support {market_event_type.value} data."
            )

        method = getattr(client, method_name)

        method(self.on_data, *symbols)

    def start_stream(self, market_data_type: MarketDataType) -> None:
        client_attr = CLIENT_MAPPING[market_data_type]
        client = getattr(self, client_attr)
        client.run()
