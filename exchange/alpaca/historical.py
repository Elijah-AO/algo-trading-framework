from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.data.requests import BaseBarsRequest, StockBarsRequest, CryptoBarsRequest
from pandas import DataFrame
from exchange.alpaca.helpers import Asset


class AlpacaHistoricalClient:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.key = api_key
        self.secret = api_secret

    def get_historical_data(
        self,
        asset: Asset,
        symbols: list[str],
        timeframe: TimeFrame,
        start: datetime,
        end: datetime,
    ) -> DataFrame:
        request_params = BaseBarsRequest(
            # may need to change if stock feed needs to be specified
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
        )

        if asset == Asset.STOCK:
            client = StockHistoricalDataClient(self.key, self.secret)
            bars = client.get_stock_bars(request_params)
            return bars.df

        elif asset == Asset.CRYPTO:
            client = CryptoHistoricalDataClient(self.key, self.secret)
            bars = client.get_crypto_bars(request_params)
            return bars.df

        else:
            raise NotImplementedError(
                "Ability for trading options/futures is not yet available in alpaca"
            )
