"""
Main Telegram bot for Binance Futures trading.
Monitors Telegram group and executes trades based on signals.
"""

import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from logger import logger
from config import config
from signal_parser import parser
from binance_trader import initialize_trader


class TradingBot:
    """Telegram bot for automated trading."""
    
    def __init__(self):
        """Initialize the trading bot."""
        self.app = None
        self.trader = None
        logger.info("🤖 Initializing Telegram Trading Bot...")
        
        # Display configuration summary
        config_summary = config.get_summary()
        logger.info(f"📋 Configuration: {config_summary}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle incoming messages from Telegram.
        
        Args:
            update: Telegram update object
            context: Telegram context
        """
        try:
            # Only process messages from the configured chat
            if str(update.effective_chat.id) != config.TELEGRAM_CHAT_ID:
                return
            
            message = update.message
            if not message or not message.text:
                return
            
            text = message.text
            logger.debug(f"📨 Received message: {text[:100]}...")
            
            # Parse signal
            signal_data = parser.parse_signal(text)
            
            if signal_data:
                logger.info("🎯 Valid trading signal detected!")
                
                # Execute trade
                success = self.trader.execute_trade(signal_data)
                
                if success:
                    # Send confirmation (optional)
                    await message.reply_text(
                        f"✅ Trade executed successfully!\n"
                        f"{signal_data['signal_type']} {signal_data['symbol']}\n"
                        f"Entry: {signal_data['entry']}, TP: {signal_data['tp']}\n"
                        f"⚠️ NO STOP LOSS - Manage risk manually"
                    )
                else:
                    await message.reply_text("❌ Failed to execute trade. Check logs for details.")
            
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}", exc_info=True)
    
    async def post_init(self, application: Application):
        """
        Post-initialization callback.
        
        Args:
            application: Telegram application
        """
        logger.info("✅ Bot initialized successfully")
        logger.info(f"👀 Monitoring chat ID: {config.TELEGRAM_CHAT_ID}")
        logger.warning("⚠️  PRODUCTION MODE - REAL TRADING ENABLED")
        logger.warning("⚠️  NO STOP LOSS PROTECTION - MANAGE RISK CAREFULLY")
    
    def run(self):
        """Start the bot."""
        try:
            # Initialize Binance trader
            logger.info("🔌 Connecting to Binance...")
            self.trader = initialize_trader()
            
            # Create Telegram application
            logger.info("🔌 Connecting to Telegram...")
            self.app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
            
            # Add message handler
            self.app.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            # Set post init callback
            self.app.post_init = self.post_init
            
            # Start the bot
            logger.info("🚀 Starting bot...")
            logger.info("=" * 50)
            logger.info("BOT IS RUNNING - Press Ctrl+C to stop")
            logger.info("=" * 50)
            
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
            raise


def main():
    """Main entry point."""
    try:
        bot = TradingBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
