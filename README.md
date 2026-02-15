# 🤖 Binance Futures Trading Bot

**⚠️ WARNING: This bot trades with REAL MONEY on Binance MAINNET**  
**⚠️ NO STOP LOSS PROTECTION - Losses can exceed your margin**  
**⚠️ Use at your own risk - Start with small amounts**

A production-ready Telegram bot that automatically monitors trading signals from a Telegram group and executes trades on Binance Futures in real-time.

## 📋 Features

- ✅ **Automatic Signal Detection** - Monitors Telegram group for LONG/SHORT signals
- ✅ **Real-time Trading** - Executes trades immediately on Binance Futures (MAINNET)
- ✅ **Take Profit Orders** - Automatically sets TP limit orders
- ⚠️ **NO Stop Loss** - SL values are parsed but NOT used (manual risk management required)
- ✅ **Leverage Trading** - Supports custom leverage from signals (1x-125x)
- ✅ **Isolated Margin** - Uses isolated margin mode for risk control
- ✅ **Comprehensive Logging** - Detailed logs of all activities
- ✅ **Safety Limits** - Configurable maximum margin per trade

## 🚨 Important Warnings

1. **REAL MONEY TRADING**: This bot operates on Binance MAINNET with real funds
2. **NO STOP LOSS**: Stop loss orders are NOT placed - you can lose your entire margin
3. **HIGH RISK**: Futures trading with leverage is extremely risky
4. **TEST FIRST**: Start with very small margin amounts to test
5. **MONITOR ACTIVELY**: Always monitor your positions manually
6. **YOUR RESPONSIBILITY**: You are fully responsible for all trades and losses

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Binance account with Futures trading enabled
- Telegram account

### Step 1: Clone Repository

```bash
git clone https://github.com/gayatrishuklaoffical-lang/binance.git
cd binance
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or using virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the **Bot Token** you receive

### Step 2: Get Telegram Chat ID

1. Add your bot to the Telegram group you want to monitor
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. Find the `chat` object and note the `id` value (this is your Chat ID)

### Step 3: Create Binance API Keys

1. Log in to [Binance](https://www.binance.com/)
2. Go to API Management (Profile → API Management)
3. Create a new API key
4. **Enable Futures Trading** permission
5. **Enable IP Access Restrictions** (recommended for security)
6. Save your **API Key** and **API Secret**

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file with your credentials:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890

# Binance API Configuration (MAINNET - REAL TRADING)
BINANCE_API_KEY=your_actual_binance_api_key
BINANCE_API_SECRET=your_actual_binance_api_secret

# Trading Configuration
MAX_MARGIN_LIMIT=100.0  # Maximum margin per trade (safety limit in USD)
```

3. **NEVER commit the `.env` file to git** - it contains sensitive credentials

## 🚀 Usage

### Start the Bot

```bash
python bot.py
```

You should see output like:
```
INFO - Configuration validated successfully
WARNING - ⚠️  RUNNING IN PRODUCTION MODE - USING BINANCE MAINNET WITH REAL FUNDS
INFO - 🤖 Initializing Telegram Trading Bot...
INFO - 🔌 Connecting to Binance...
INFO - ✅ Connected to Binance Futures
INFO - 💰 Total Wallet Balance: $XXX.XX USDT
INFO - 🔌 Connecting to Telegram...
INFO - 🚀 Starting bot...
INFO - BOT IS RUNNING - Press Ctrl+C to stop
```

### Signal Format

The bot monitors for messages in this format:

**LONG Signal:**
```
🟢 LONG SIGNAL - SOLUSDT

Entry: 87.50000
TP: 88.37500 (1%)
SL: 87.06250 (0.5%)

Leverage: 3x
Margin: $5

Est Profit: $0.15
Est Loss: $0.075
```

**SHORT Signal:**
```
🔴 SHORT SIGNAL - SOLUSDT

Entry: 87.50000
TP: 86.62500 (1%)
SL: 87.93750 (0.5%)

Leverage: 3x
Margin: $5

Est Profit: $0.15
Est Loss: $0.075
```

### What Happens When Signal is Detected

1. ✅ Bot parses the signal and validates data
2. ✅ Checks your Binance account balance
3. ✅ Sets leverage to specified value (e.g., 3x)
4. ✅ Places MARKET entry order (BUY for LONG, SELL for SHORT)
5. ✅ Places TAKE PROFIT order at TP price
6. ⚠️ **Does NOT place Stop Loss order** - SL is ignored

### Stop the Bot

Press `Ctrl+C` to stop the bot gracefully.

## 📊 Monitoring

### View Logs

Logs are stored in the `logs/` directory:
- `logs/bot.log` - Main log file with all activities
- Log files rotate automatically (10MB max, 5 backups)

View real-time logs:
```bash
tail -f logs/bot.log
```

### Check Running Status

The bot logs every action:
- Signal detection
- Order placement
- Errors and warnings
- Balance checks

## 🔒 Security Best Practices

### API Key Security

1. ✅ **Restrict API Permissions**: Enable ONLY "Futures Trading" permission
2. ✅ **IP Whitelist**: Add your server IP to Binance API whitelist
3. ✅ **Never Share**: Keep your API keys private
4. ✅ **Rotate Keys**: Change API keys periodically
5. ✅ **Two-Factor Auth**: Enable 2FA on your Binance account

### Trading Safety

1. ✅ **Start Small**: Begin with minimum margin amounts ($1-5)
2. ✅ **Test First**: Test with small trades before using larger amounts
3. ✅ **Set Limits**: Use MAX_MARGIN_LIMIT to prevent large trades
4. ⚠️ **Manual SL**: Since bot doesn't place SL, set manual stop losses
5. ✅ **Monitor Positions**: Regularly check your open positions
6. ✅ **Keep Reserves**: Don't use your entire balance for margin

### Environment Security

1. ✅ **Never commit `.env`**: Already in `.gitignore`
2. ✅ **Secure Server**: Use a secure server for running the bot
3. ✅ **Regular Updates**: Keep dependencies updated
4. ✅ **Backup Logs**: Regular backup of log files for audit trail

## 🛠️ Troubleshooting

### Bot doesn't start

**Problem**: Missing environment variables
```
ValueError: Missing required environment variables: TELEGRAM_BOT_TOKEN
```

**Solution**: Ensure all variables in `.env` are set correctly

---

**Problem**: Invalid Binance API credentials
```
❌ Failed to connect to Binance: API-key format invalid
```

**Solution**: 
- Verify API key and secret are correct
- Ensure Futures trading permission is enabled
- Check if IP is whitelisted (if restriction enabled)

---

### Signal not detected

**Problem**: Bot receives message but doesn't execute trade

**Solution**:
- Check signal format matches exactly (including emojis 🟢/🔴)
- Verify TELEGRAM_CHAT_ID matches the group
- Check logs for parsing errors

---

### Insufficient balance

**Problem**: 
```
❌ Insufficient balance: $10.00 available, $50.00 required
```

**Solution**: 
- Deposit more USDT to Futures wallet
- Or reduce margin amount in signals

---

### Order placement fails

**Problem**: Market order placed but TP fails

**Solution**:
- Manually set TP on Binance
- Check if position is still open
- Verify symbol exists and is trading

---

### Leverage error

**Problem**:
```
❌ Failed to set leverage: Invalid leverage
```

**Solution**:
- Some pairs have maximum leverage limits (e.g., 20x)
- Reduce leverage in signal
- Check Binance limits for specific symbol

## 📁 Project Structure

```
binance/
├── bot.py                 # Main entry point - Telegram bot
├── signal_parser.py       # Parse trading signals from messages
├── binance_trader.py      # Binance Futures trading logic
├── config.py              # Configuration and environment variables
├── logger.py              # Logging setup with rotation
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual credentials (not in git)
├── .gitignore            # Ignore sensitive files
├── logs/                  # Log files directory (auto-created)
│   └── bot.log           # Main log file
└── README.md             # This file
```

## 🧪 Testing

### Test Signal Parsing

Send a test signal in your Telegram group to verify parsing:
- Check logs for "✅ Parsed LONG/SHORT signal"
- Verify all values are extracted correctly

### Test with Small Amount

Before using real amounts:
1. Set `MAX_MARGIN_LIMIT=1.0` in `.env`
2. Send signal with `Margin: $1`
3. Verify trade executes correctly
4. Check on Binance Futures that position opened

### Verify Orders

After signal execution, check Binance:
1. Open Positions tab - verify position opened
2. Open Orders tab - verify TP order is set
3. **Manually set a Stop Loss** - bot doesn't do this!

## ⚖️ Risk Management

Since this bot does **NOT place Stop Loss orders**, you MUST manage risk manually:

### Manual Stop Loss

1. After bot opens position, immediately go to Binance
2. Set a manual Stop Loss order
3. Use the SL value from signal as reference (or your own)

### Position Monitoring

- Set price alerts on Binance mobile app
- Check positions regularly
- Have a plan for closing losing positions

### Capital Management

- Never risk more than 1-2% of capital per trade
- Use appropriate leverage (lower is safer)
- Keep emergency reserves

## 📚 Additional Resources

- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Binance Futures Trading Guide](https://www.binance.com/en/support/faq/futures-trading)

## 🤝 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs in `logs/bot.log`
3. Ensure all configuration is correct
4. Verify API keys have correct permissions

## ⚖️ Disclaimer

**THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.**

- This bot is for educational purposes
- Trading cryptocurrencies and futures is highly risky
- You can lose all your invested capital
- The developers are not responsible for any financial losses
- Always do your own research (DYOR)
- Never invest more than you can afford to lose
- **This bot does not place Stop Loss orders - manage your risk manually**

## 📄 License

This project is open source and available under the MIT License.

---

**Made with ❤️ for automated trading enthusiasts**

**Remember: With great automation comes great responsibility! 🚀**
