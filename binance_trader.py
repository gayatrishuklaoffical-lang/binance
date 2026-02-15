"""
Binance Futures trading logic.
Handles order placement and execution on Binance Futures MAINNET.
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException
from typing import Dict, Optional
from logger import logger
from config import config


class BinanceTrader:
    """Handle Binance Futures trading operations."""
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance Futures client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.client = Client(api_key, api_secret)
        logger.info("🔌 Binance Futures client initialized (MAINNET)")
        
        # Verify connection and permissions
        self._verify_connection()
    
    def _verify_connection(self):
        """Verify API connection and futures trading permissions."""
        try:
            # Test connectivity
            account_info = self.client.futures_account()
            balance = float(account_info['totalWalletBalance'])
            logger.info(f"✅ Connected to Binance Futures")
            logger.info(f"💰 Total Wallet Balance: ${balance:.2f} USDT")
            logger.warning("⚠️  TRADING WITH REAL FUNDS ON MAINNET")
        except BinanceAPIException as e:
            logger.error(f"❌ Failed to connect to Binance: {e}")
            raise
    
    def set_leverage(self, symbol: str, leverage: int) -> bool:
        """
        Set leverage for a trading pair.
        
        Args:
            symbol: Trading pair symbol (e.g., 'SOLUSDT')
            leverage: Leverage value (1-125)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.futures_change_leverage(
                symbol=symbol,
                leverage=leverage
            )
            logger.info(f"🔧 Set leverage to {leverage}x for {symbol}")
            return True
        except BinanceAPIException as e:
            logger.error(f"❌ Failed to set leverage: {e}")
            return False
    
    def set_margin_type(self, symbol: str, margin_type: str = 'ISOLATED') -> bool:
        """
        Set margin type for a trading pair.
        
        Args:
            symbol: Trading pair symbol
            margin_type: 'ISOLATED' or 'CROSSED'
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.futures_change_margin_type(
                symbol=symbol,
                marginType=margin_type
            )
            logger.info(f"🔧 Set margin type to {margin_type} for {symbol}")
            return True
        except BinanceAPIException as e:
            # Error code -4046 means margin type is already set
            if e.code == -4046:
                logger.info(f"ℹ️  Margin type already set to {margin_type} for {symbol}")
                return True
            logger.error(f"❌ Failed to set margin type: {e}")
            return False
    
    def calculate_quantity(self, symbol: str, margin: float, leverage: int, entry_price: float) -> float:
        """
        Calculate order quantity based on margin and leverage.
        
        Args:
            symbol: Trading pair symbol
            margin: Margin amount in USD
            leverage: Leverage multiplier
            entry_price: Entry price
            
        Returns:
            Calculated quantity
        """
        try:
            # Get symbol info for precision
            exchange_info = self.client.futures_exchange_info()
            symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)
            
            if not symbol_info:
                raise ValueError(f"Symbol {symbol} not found")
            
            # Calculate position size
            position_size = margin * leverage
            quantity = position_size / entry_price
            
            # Get quantity precision
            quantity_precision = 0
            for symbol_filter in symbol_info['filters']:
                if symbol_filter['filterType'] == 'LOT_SIZE':
                    step_size = float(symbol_filter['stepSize'])
                    # Calculate precision from step size
                    quantity_precision = len(str(step_size).rstrip('0').split('.')[-1])
                    break
            
            # Round to appropriate precision
            quantity = round(quantity, quantity_precision)
            
            logger.info(f"📊 Calculated quantity: {quantity} {symbol.replace('USDT', '')}")
            logger.info(f"   Position size: ${position_size:.2f} (Margin: ${margin} × {leverage}x)")
            
            return quantity
            
        except Exception as e:
            logger.error(f"❌ Error calculating quantity: {e}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Optional[Dict]:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair symbol
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            Order response if successful, None otherwise
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"✅ Market order placed: {side} {quantity} {symbol}")
            logger.info(f"   Order ID: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"❌ Failed to place market order: {e}")
            return None
    
    def place_tp_order(self, symbol: str, side: str, quantity: float, tp_price: float) -> Optional[Dict]:
        """
        Place a Take Profit limit order.
        
        Args:
            symbol: Trading pair symbol
            side: 'SELL' for LONG, 'BUY' for SHORT
            quantity: Order quantity
            tp_price: Take profit price
            
        Returns:
            Order response if successful, None otherwise
        """
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='TAKE_PROFIT_MARKET',
                quantity=quantity,
                stopPrice=tp_price,
                closePosition=True
            )
            
            logger.info(f"✅ Take Profit order placed: {side} {quantity} {symbol} @ {tp_price}")
            logger.info(f"   Order ID: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"❌ Failed to place TP order: {e}")
            return None
    
    def check_balance(self, required_margin: float) -> bool:
        """
        Check if account has sufficient balance.
        
        Args:
            required_margin: Required margin amount
            
        Returns:
            True if sufficient balance, False otherwise
        """
        try:
            account_info = self.client.futures_account()
            available_balance = float(account_info['availableBalance'])
            
            if available_balance >= required_margin:
                logger.info(f"✅ Sufficient balance: ${available_balance:.2f} available, ${required_margin:.2f} required")
                return True
            else:
                logger.error(f"❌ Insufficient balance: ${available_balance:.2f} available, ${required_margin:.2f} required")
                return False
                
        except BinanceAPIException as e:
            logger.error(f"❌ Failed to check balance: {e}")
            return False
    
    def execute_trade(self, signal_data: Dict) -> bool:
        """
        Execute a trade based on signal data.
        Places market entry order + TP order only (NO stop loss).
        
        Args:
            signal_data: Dictionary with signal information
            
        Returns:
            True if trade executed successfully, False otherwise
        """
        try:
            symbol = signal_data['symbol']
            signal_type = signal_data['signal_type']
            entry = signal_data['entry']
            tp = signal_data['tp']
            leverage = signal_data['leverage']
            margin = signal_data['margin']
            
            logger.info(f"🚀 Executing {signal_type} trade for {symbol}")
            
            # Safety check: max margin limit
            if margin > config.MAX_MARGIN_LIMIT:
                logger.error(f"❌ Margin ${margin} exceeds safety limit ${config.MAX_MARGIN_LIMIT}")
                return False
            
            # Check balance
            if not self.check_balance(margin):
                return False
            
            # Set margin type to ISOLATED
            if not self.set_margin_type(symbol, 'ISOLATED'):
                logger.warning("⚠️  Failed to set margin type, continuing anyway...")
            
            # Set leverage
            if not self.set_leverage(symbol, leverage):
                return False
            
            # Calculate quantity
            quantity = self.calculate_quantity(symbol, margin, leverage, entry)
            
            # Determine order sides
            if signal_type == 'LONG':
                entry_side = 'BUY'
                tp_side = 'SELL'
            else:  # SHORT
                entry_side = 'SELL'
                tp_side = 'BUY'
            
            # Place market entry order
            logger.info(f"📍 Step 1/2: Placing market entry order...")
            entry_order = self.place_market_order(symbol, entry_side, quantity)
            if not entry_order:
                logger.error("❌ Failed to place entry order, aborting trade")
                return False
            
            # Place TP order
            logger.info(f"📍 Step 2/2: Placing Take Profit order...")
            tp_order = self.place_tp_order(symbol, tp_side, quantity, tp)
            if not tp_order:
                logger.error("⚠️  Entry order placed but TP order failed!")
                logger.warning("⚠️  You may need to set TP manually")
                return False
            
            # Note: NO Stop Loss order is placed (as per requirements)
            logger.warning("⚠️  NO STOP LOSS ORDER - Position is not protected by SL")
            
            logger.info(f"✅ Trade executed successfully!")
            logger.info(f"   {signal_type} {symbol} - Entry: {entry}, TP: {tp}")
            logger.info(f"   Leverage: {leverage}x, Margin: ${margin}, Quantity: {quantity}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing trade: {e}")
            return False


# Create trader instance (will be initialized in bot.py)
trader = None


def initialize_trader():
    """Initialize the Binance trader with credentials from config."""
    global trader
    trader = BinanceTrader(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
    return trader
