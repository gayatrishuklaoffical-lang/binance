"""
Main Telegram bot for Binance Futures trading.
Monitors Telegram channels and groups and executes trades based on signals.
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
        """Handle incoming messages from Telegram (both groups and channels).
        
        Args:
            update: Telegram update object
            context: Telegram context
        """
        try:
            # Only process messages from the configured chat
            if str(update.effective_chat.id) != config.TELEGRAM_CHAT_ID:
                return
            
            # Support both regular messages and channel posts
            message = update.message or update.channel_post
            if not message or not message.text:
                return
            
            text = message.text
            logger.info(f"📨 Received message from chat {update.effective_chat.id}")
            logger.debug(f"Message text: {text[:100]}...")
            
            # Parse signal
            signal_data = parser.parse_signal(text)
            
            if signal_data:
                logger.info("🎯 Valid trading signal detected!")
                logger.info(f"📊 Signal: {signal_data['signal_type']} {signal_data['symbol']} | Entry: {signal_data['entry']} | TP: {signal_data['tp']} | Leverage: {signal_data['leverage']}x | Margin: ${signal_data['margin']}")
                
                # Execute trade
                success = self.trader.execute_trade(signal_data)
                
                if success:
                    logger.info("✅ Trade executed successfully!")
                    # Note: Channels don't support reply_text, so we just log
                    if update.message:  # Only reply in groups, not channels
                        try:
                            await message.reply_text(
                                f"✅ Trade executed successfully!\n"
                                f"{signal_data['signal_type']} {signal_data['symbol']}\n"
                                f"Entry: {signal_data['entry']}, TP: {signal_data['tp']}\n"
                                f"⚠️ NO STOP LOSS - Manage risk manually"
                            )
                        except Exception as e:
                            logger.warning(f"Could not send reply (might be a channel): {e}")
                else:
                    logger.error("❌ Failed to execute trade")
            else:
                logger.debug("Message is not a valid trading signal")
            
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}", exc_info=True)
    
    async def handle_channel_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle channel posts specifically.
        
        Args:
            update: Telegram update object
            context: Telegram context
        """
        # Reuse the same message handler
        await self.handle_message(update, context)
    
    async def post_init(self, application: Application):
        """Post-initialization callback.
        
        Args:
            application: Telegram application
        """
        logger.info("✅ Bot initialized successfully")
        logger.info(f"👀 Monitoring chat ID: {config.TELEGRAM_CHAT_ID}")
        logger.info("📢 Supports both Groups and Channels")
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
            
            # Add message handler for regular messages (groups)
            self.app.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            # Add handler for channel posts
            self.app.add_handler(
                MessageHandler(filters.UpdateType.CHANNEL_POST, self.handle_channel_post)
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