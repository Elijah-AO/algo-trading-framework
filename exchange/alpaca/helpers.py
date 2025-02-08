from enum import Enum
from alpaca.data.requests import (
    CorporateActionsRequest,
    StockBarsRequest,
    StockTradesRequest,
    StockQuotesRequest,
    CryptoQuoteRequest,
    CryptoBarsRequest,
    CryptoTradesRequest,
    OptionBarsRequest,
    OptionTradesRequest,
    NewsRequest,
)

from alpaca.data.live.stock import StockDataStream

REQUEST_LIMIT = 1000


class MarketDataType(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    OPTION = "option"
    CORPORATE_ACTION = "corporate_action"
    FOREX = "forex"
    NEWS = "news"
    FUTURE = "future"  # unsupported as of now


class MarketEventType(Enum):
    QUOTE = "quote"
    BAR = "bar"
    TRADE = "trade"
    NEWS = "news"
    DAILY_BAR = "daily_bar"
    UPDATED_BAR = "updated_bar"
    ORDERBOOK = "orderbook"
    TRADING_STATUS = "trading_status"
    TRADE_CORRECTION = "trade_correction"
    TRADE_CANCEL = "trade_cancel"
    CORPORATE_ACTION = "corporate_action"


# May need to split into live/historical client
CLIENT_MAPPING = {
    MarketDataType.STOCK: "stock_client",
    MarketDataType.CRYPTO: "crypto_client",
    MarketDataType.OPTION: "option_client",
    MarketDataType.NEWS: "news_client",
}

HISTORICAL_REQUEST_CLASSES = {
    MarketDataType.STOCK: {
        MarketEventType.BAR: StockBarsRequest,
        MarketEventType.QUOTE: StockQuotesRequest,
        MarketEventType.TRADE: StockTradesRequest,
    },
    MarketDataType.CRYPTO: {
        MarketEventType.BAR: CryptoBarsRequest,
        MarketEventType.QUOTE: CryptoQuoteRequest,
        MarketEventType.TRADE: CryptoTradesRequest,
    },
    MarketDataType.OPTION: {
        MarketEventType.BAR: OptionBarsRequest,
        MarketEventType.TRADE: OptionTradesRequest,
    },
    MarketDataType.NEWS: {MarketEventType.NEWS: NewsRequest},
    MarketDataType.CORPORATE_ACTION: {
        MarketEventType.CORPORATE_ACTION: CorporateActionsRequest
    },
}

LIVE_REQUEST_CLASSES = {
    MarketDataType.STOCK: {
        MarketEventType.BAR,
        MarketEventType.QUOTE,
        MarketEventType.TRADE,
        MarketEventType.DAILY_BAR,
        MarketEventType.UPDATED_BAR,
        MarketEventType.TRADING_STATUS,
        MarketEventType.TRADE_CORRECTION,
        MarketEventType.TRADE_CANCEL,
    },
    MarketDataType.CRYPTO: {
        MarketEventType.BAR,
        MarketEventType.QUOTE,
        MarketEventType.TRADE,
        MarketEventType.DAILY_BAR,
        MarketEventType.UPDATED_BAR,
        MarketEventType.ORDERBOOK,
    },
    MarketDataType.OPTION: {
        MarketEventType.QUOTE,
        MarketEventType.TRADE,
    },
    MarketDataType.NEWS: {MarketEventType.NEWS},
}
