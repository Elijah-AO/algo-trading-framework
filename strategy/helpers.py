from enum import Enum
from dataclasses import dataclass

from exchange.alpaca.helpers import MarketDataType


class Signal(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Instrument:
    symbol: str
    market_data_type: MarketDataType
