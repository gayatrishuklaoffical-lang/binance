"""
Configuration management for the Binance Futures Trading Bot.
Loads and validates environment variables.
"""

import os
from dotenv import load_dotenv
from logger import logger

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage bot settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Telegram Configuration
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        
        # Binance API Configuration (MAINNET)
        self.BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
        self.BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
        
        # Trading Configuration
        self.MAX_MARGIN_LIMIT = float(os.getenv('MAX_MARGIN_LIMIT', '100.0'))
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """Validate that all required configuration variables are set."""
        required_vars = {
            'TELEGRAM_BOT_TOKEN': self.TELEGRAM_BOT_TOKEN,
            'TELEGRAM_CHAT_ID': self.TELEGRAM_CHAT_ID,
            'BINANCE_API_KEY': self.BINANCE_API_KEY,
            'BINANCE_API_SECRET': self.BINANCE_API_SECRET,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("Configuration validated successfully")
        logger.warning("⚠️  RUNNING IN PRODUCTION MODE - USING BINANCE MAINNET WITH REAL FUNDS")
    
    def get_summary(self):
        """Get a summary of the configuration (without secrets)."""
        return {
            'telegram_configured': bool(self.TELEGRAM_BOT_TOKEN),
            'binance_configured': bool(self.BINANCE_API_KEY),
            'max_margin_limit': self.MAX_MARGIN_LIMIT,
            'mode': 'PRODUCTION (MAINNET)',
        }


# Create singleton configuration instance
config = Config()
