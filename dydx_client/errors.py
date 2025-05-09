# Define custom exceptions
class DydxError(Exception):
    """Base exception for all dYdX-related errors"""
    pass


class InvalidWallet(DydxError):
    """Exception raised when an order price is invalid or outside acceptable range"""

    def __init__(self, message="Invalid wallet address", address=None):
        self.message = f"{message}: wallet address {address} is not valid"
        super().__init__(self.message)


class InvalidMnemonic(DydxError):
    """Exception raised when an order price is invalid or outside acceptable range"""

    def __init__(self, message="Invalid mnemonic phrase"):
        self.message = f"{message}: mneumonic phrase is not valid"
        super().__init__(self.message)


class InvalidPrice(DydxError):
    """Exception raised when an order price is invalid or outside acceptable range"""

    def __init__(self, message="Order price is invalid or outside acceptable range", market=None, side=None, price=None,
                 oracle_price=None):
        self.market = market
        self.side = side
        self.price = price
        self.oracle_price = oracle_price
        self.message = message
        if all([market, side, price, oracle_price]):
            self.message = f"{message}: {side} order on {market} at price {price} (oracle price: {oracle_price})"
        super().__init__(self.message)


class ReduceOnlyOrderError(DydxError):
    """Exception raised when a reduce-only order fails due to specific restrictions"""

    def __init__(self, message="Reduce-only order failed", code=None, raw_log=None, tx_hash=None):
        self.code = code
        self.raw_log = raw_log
        self.tx_hash = tx_hash
        self.message = message

        # Add more details if provided
        if raw_log:
            self.message = f"{message}: {raw_log}"
        if code:
            self.message = f"{self.message} (Error code: {code})"
        if tx_hash:
            self.message = f"{self.message} [TX: {tx_hash}]"

        super().__init__(self.message)


class OrderRejected(DydxError):
    """Exception raised when an order is rejected by the API"""

    def __init__(self, message="Order was rejected", response=None):
        self.response = response
        self.message = message
        if response:
            self.message = f"{message}: {response}"
        super().__init__(self.message)


class NetworkError(DydxError):
    """Exception raised for network-related issues"""
    pass


class AuthenticationError(DydxError):
    """Exception raised for authentication issues"""
    pass