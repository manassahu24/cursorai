import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', 'demo')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading_system.db')
    
    # Trading Parameters
    MIN_MARKET_CAP = 1000000000  # $1B minimum market cap
    MIN_VOLUME = 1000000  # 1M minimum volume
    MAX_PE_RATIO = 50
    MIN_PE_RATIO = 5
    MAX_DEBT_TO_EQUITY = 2.0
    MIN_CURRENT_RATIO = 1.0
    MIN_ROE = 0.10  # 10% minimum ROE
    
    # Technical Analysis Parameters
    SHORT_TERM_MA = 20
    LONG_TERM_MA = 50
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # Sector Analysis
    SECTORS = [
        'Technology', 'Healthcare', 'Financial Services', 'Consumer Cyclical',
        'Industrials', 'Consumer Defensive', 'Energy', 'Basic Materials',
        'Real Estate', 'Communication Services', 'Utilities'
    ]
    
    # Risk Management
    MAX_POSITION_SIZE = 0.05  # 5% max position size
    STOP_LOSS_PERCENTAGE = 0.10  # 10% stop loss
    TAKE_PROFIT_PERCENTAGE = 0.20  # 20% take profit
    
    # Data Sources
    STOCK_LIST_URL = "https://www.nasdaq.com/market-activity/stocks/screener"
    SECTOR_PERFORMANCE_URL = "https://www.sectorspdr.com/sectorspdr/tools/sector-tracker"