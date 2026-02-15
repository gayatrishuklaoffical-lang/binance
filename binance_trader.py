import logging

# Assuming this is part of the Binance trader class
class BinanceTrader:
    # Other methods...

    def has_open_positions(self):
        # Fetch open positions from Binance Futures
        positions = self.client.futures_position_information()
        open_positions = []

        for position in positions:
            if float(position['positionAmt']) != 0:
                open_positions.append(position)
                logging.info(f"Open Position - Symbol: {position['symbol']}, Amount: {position['positionAmt']}, Entry Price: {position['entryPrice']}, Unrealized PnL: {position['unrealizedProfit']}")

        return len(open_positions) > 0

    def execute_trade(self, *args, **kwargs):
        if self.has_open_positions():
            logging.error("🛑 TRADE BLOCKED: Existing position(s) must be closed first")
            return False
        # Proceed with trade execution logic...

# Configure logging
logging.basicConfig(level=logging.INFO)
