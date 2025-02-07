from enum import Enum
from alpaca.data.requests import (
    StockBarsRequest,
    StockTradesRequest,
    StockQuotesRequest,
    CryptoQuoteRequest,
    CryptoBarsRequest,
    CryptoTradesRequest,
    OptionBarsRequest,
    OptionTradesRequest,
)


class MarketDataType(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    OPTION = "option"
    FUTURE = "future"
    NEWS = "news"


class MarketEventType(Enum):
    QUOTE = "quote"
    BAR = "bar"
    TRADE = "trade"


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
}

HISTORICAL_CLIENT_MAPPING = {
    MarketDataType.STOCK: "stock_client",
    MarketDataType.CRYPTO: "crypto_client",
    MarketDataType.OPTION: "option_client",
}

REQUEST_LIMIT = 1000
