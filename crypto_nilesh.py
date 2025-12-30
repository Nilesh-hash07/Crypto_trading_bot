import logging
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

# ---------------- LOGGING CONFIG ---------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("trading_bot.log"),
        logging.StreamHandler()
    ]
)

# ---------------- BASIC TRADING BOT ---------------- #
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        logging.info("Binance Futures Testnet client initialized")

    # ---------- MARKET ORDER ---------- #
    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            logging.info(f"Market order placed: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error(f"Market order error: {e}")
            return None

    # ---------- LIMIT ORDER ---------- #
    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit order placed: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error(f"Limit order error: {e}")
            return None

    # ---------- STOP-LIMIT ORDER (BONUS) ---------- #
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce="GTC"
            )
            logging.info(f"Stop-Limit order placed: {order}")
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error(f"Stop-Limit order error: {e}")
            return None


# ---------------- CLI INTERFACE ---------------- #
def validate_side(side):
    return side.upper() in ["BUY", "SELL"]

def main():
    print("\n=== Binance Futures Testnet Trading Bot ===\n")

    api_key = input("Enter API Key: ").strip()
    api_secret = input("Enter API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    symbol = input("Trading Pair (e.g., BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()

    if not validate_side(side):
        print("❌ Invalid side. Use BUY or SELL.")
        return

    print("\nOrder Types:")
    print("1. Market")
    print("2. Limit")
    print("3. Stop-Limit (Bonus)")

    order_type = input("Choose order type (1/2/3): ").strip()

    try:
        quantity = float(input("Quantity: "))

        if order_type == "1":
            result = bot.place_market_order(symbol, side, quantity)

        elif order_type == "2":
            price = float(input("Limit Price: "))
            result = bot.place_limit_order(symbol, side, quantity, price)

        elif order_type == "3":
            stop_price = float(input("Stop Price: "))
            limit_price = float(input("Limit Price: "))
            result = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)

        else:
            print("❌ Invalid order type")
            return

        if result:
            print("\n✅ Order Placed Successfully")
            print(f"Order ID: {result['orderId']}")
            print(f"Status: {result['status']}")
            print(f"Executed Qty: {result['executedQty']}")
        else:
            print("\n❌ Order failed. Check logs.")

    except ValueError:
        print("❌ Invalid numeric input")

if __name__ == "__main__":
    main()
