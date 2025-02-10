from enum import Enum
from alpaca.data.requests import (
    CorporateActionsRequest,
    CryptoLatestOrderbookRequest,
    CryptoLatestQuoteRequest,
    CryptoLatestTradeRequest,
    CryptoSnapshotRequest,
    OptionChainRequest,
    OptionLatestQuoteRequest,
    OptionLatestTradeRequest,
    OptionSnapshotRequest,
    StockBarsRequest,
    StockLatestBarRequest,
    StockLatestQuoteRequest,
    StockLatestTradeRequest,
    StockSnapshotRequest,
    StockTradesRequest,
    StockQuotesRequest,
    CryptoQuoteRequest,
    CryptoBarsRequest,
    CryptoTradesRequest,
    CryptoLatestBarRequest,
    CryptoLatestOrderbookRequest,
    CryptoSnapshotRequest,
    CryptoLatestTradeRequest,
    CryptoLatestQuoteRequest,
    OptionBarsRequest,
    OptionTradesRequest,
    NewsRequest,
)

from alpaca.data.live.stock import StockDataStream

# consider removing
REQUEST_LIMIT = 1000


class MarketDataType(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    OPTION = "option"
    CORPORATE_ACTIONS = "corporate_actions"
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
    CORPORATE_ACTIONS = "corporate_actions"
    SNAPSHOT = "snapshot"
    CHAIN = "chain"
    # TODO: ADD -> EXCHANGE_CODES = "exchange_codes"


# May need to split into live/historical client
CLIENT_MAPPING = {
    MarketDataType.STOCK: "stock_client",
    MarketDataType.CRYPTO: "crypto_client",
    MarketDataType.OPTION: "option_client",
    MarketDataType.NEWS: "news_client",
    MarketDataType.CORPORATE_ACTIONS: "corporate_action_client",
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
    MarketDataType.CORPORATE_ACTIONS: {
        MarketEventType.CORPORATE_ACTIONS: CorporateActionsRequest
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

LATEST_REQUEST_CLASSES = {
    MarketDataType.STOCK: {
        MarketEventType.BAR: StockLatestBarRequest,
        MarketEventType.QUOTE: StockLatestQuoteRequest,
        MarketEventType.TRADE: StockLatestTradeRequest,
        MarketEventType.SNAPSHOT: StockSnapshotRequest,
    },
    MarketDataType.CRYPTO: {
        MarketEventType.BAR: CryptoLatestBarRequest,
        MarketEventType.QUOTE: CryptoLatestQuoteRequest,
        MarketEventType.TRADE: CryptoLatestTradeRequest,
        MarketEventType.ORDERBOOK: CryptoLatestOrderbookRequest,
        MarketEventType.SNAPSHOT: CryptoSnapshotRequest,
    },
    MarketDataType.OPTION: {
        MarketEventType.QUOTE: OptionLatestQuoteRequest,
        MarketEventType.TRADE: OptionLatestTradeRequest,
        MarketEventType.SNAPSHOT: OptionSnapshotRequest,
        MarketEventType.CHAIN: OptionChainRequest,
    },
}
