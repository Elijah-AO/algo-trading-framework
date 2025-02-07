from enum import Enum


class Asset(Enum):
    # May need to extend for options/futures

    STOCK = "stock"
    CRYPTO = "crypto"
    OPTION = "option"
    FUTURE = "future"


class Endpoint(Enum):
    pass
