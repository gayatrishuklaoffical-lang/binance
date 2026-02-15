"""
Signal parser for Telegram trading signals.
Extracts trading information from LONG and SHORT signal messages.
"""

import re
from typing import Optional, Dict
from logger import logger


class SignalParser:
    """Parse trading signals from Telegram messages."""
    
    # Regex patterns for signal parsing
    LONG_PATTERN = r'🟢\s*LONG\s+SIGNAL\s*-\s*([A-Z]+)'
    SHORT_PATTERN = r'🔴\s*SHORT\s+SIGNAL\s*-\s*([A-Z]+)'
    ENTRY_PATTERN = r'Entry:\s*([\d.]+)'
    TP_PATTERN = r'TP:\s*([\d.]+)'
    SL_PATTERN = r'SL:\s*([\d.]+)'
    LEVERAGE_PATTERN = r'Leverage:\s*(\d+)x'
    MARGIN_PATTERN = r'Margin:\s*\$\s*([\d.]+)'
    
    @staticmethod
    def parse_signal(message: str) -> Optional[Dict]:
        """
        Parse a trading signal from a message.
        
        Args:
            message: The message text to parse
            
        Returns:
            Dictionary with signal data if valid, None otherwise
            Keys: signal_type, symbol, entry, tp, sl, leverage, margin
        """
        if not message:
            return None
        
        # Detect signal type
        long_match = re.search(SignalParser.LONG_PATTERN, message, re.IGNORECASE)
        short_match = re.search(SignalParser.SHORT_PATTERN, message, re.IGNORECASE)
        
        if long_match:
            signal_type = 'LONG'
            symbol = long_match.group(1)
        elif short_match:
            signal_type = 'SHORT'
            symbol = short_match.group(1)
        else:
            # Not a valid signal
            return None
        
        # Extract signal parameters
        entry_match = re.search(SignalParser.ENTRY_PATTERN, message)
        tp_match = re.search(SignalParser.TP_PATTERN, message)
        sl_match = re.search(SignalParser.SL_PATTERN, message)
        leverage_match = re.search(SignalParser.LEVERAGE_PATTERN, message)
        margin_match = re.search(SignalParser.MARGIN_PATTERN, message)
        
        # Validate required fields
        if not all([entry_match, tp_match, leverage_match, margin_match]):
            logger.warning(f"Incomplete signal data in message: {message[:100]}")
            return None
        
        try:
            signal_data = {
                'signal_type': signal_type,
                'symbol': symbol,
                'entry': float(entry_match.group(1)),
                'tp': float(tp_match.group(1)),
                'sl': float(sl_match.group(1)) if sl_match else None,  # Parse SL but will not use it
                'leverage': int(leverage_match.group(1)),
                'margin': float(margin_match.group(1)),
            }
            
            # Validate extracted data
            if SignalParser.validate_signal(signal_data):
                logger.info(f"✅ Parsed {signal_type} signal for {symbol}")
                logger.info(f"   Entry: {signal_data['entry']}, TP: {signal_data['tp']}, "
                          f"Leverage: {signal_data['leverage']}x, Margin: ${signal_data['margin']}")
                if signal_data['sl']:
                    logger.info(f"   SL: {signal_data['sl']} (parsed but will NOT be used for trading)")
                return signal_data
            else:
                return None
                
        except (ValueError, AttributeError) as e:
            logger.error(f"Error parsing signal values: {e}")
            return None
    
    @staticmethod
    def validate_signal(signal_data: Dict) -> bool:
        """
        Validate signal data for correctness.
        
        Args:
            signal_data: Dictionary with signal data
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields exist
            required_fields = ['signal_type', 'symbol', 'entry', 'tp', 'leverage', 'margin']
            if not all(field in signal_data for field in required_fields):
                logger.error("Missing required fields in signal data")
                return False
            
            # Validate numeric values
            if signal_data['entry'] <= 0:
                logger.error("Entry price must be positive")
                return False
            
            if signal_data['tp'] <= 0:
                logger.error("TP price must be positive")
                return False
            
            if signal_data['leverage'] < 1 or signal_data['leverage'] > 125:
                logger.error(f"Invalid leverage: {signal_data['leverage']} (must be 1-125)")
                return False
            
            if signal_data['margin'] <= 0:
                logger.error("Margin must be positive")
                return False
            
            # Validate TP direction
            if signal_data['signal_type'] == 'LONG':
                if signal_data['tp'] <= signal_data['entry']:
                    logger.error(f"LONG TP ({signal_data['tp']}) must be above entry ({signal_data['entry']})")
                    return False
            elif signal_data['signal_type'] == 'SHORT':
                if signal_data['tp'] >= signal_data['entry']:
                    logger.error(f"SHORT TP ({signal_data['tp']}) must be below entry ({signal_data['entry']})")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating signal: {e}")
            return False


# Create parser instance
parser = SignalParser()
