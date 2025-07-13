import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import aiohttp
from config import Config

class DataCollector:
    def __init__(self):
        self.config = Config()
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_fundamental_data(self, symbol: str) -> Dict:
        """Fetch fundamental data for a stock"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            fundamental_data = {
                'symbol': symbol,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'price_to_book': info.get('priceToBook', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'roe': info.get('returnOnEquity', 0),
                'roa': info.get('returnOnAssets', 0),
                'profit_margins': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'beta': info.get('beta', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0)
            }
            return fundamental_data
        except Exception as e:
            print(f"Error fetching fundamental data for {symbol}: {e}")
            return {}
    
    async def get_multiple_stocks_data(self, symbols: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple stocks asynchronously"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for symbol in symbols:
                task = self._fetch_stock_data_async(session, symbol)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            data_dict = {}
            for symbol, result in zip(symbols, results):
                if isinstance(result, pd.DataFrame) and not result.empty:
                    data_dict[symbol] = result
            
            return data_dict
    
    async def _fetch_stock_data_async(self, session: aiohttp.ClientSession, symbol: str) -> pd.DataFrame:
        """Async helper to fetch stock data"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'range': '1y',
                'interval': '1d',
                'includePrePost': 'false'
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # Parse Yahoo Finance data
                    timestamps = data['chart']['result'][0]['timestamp']
                    quotes = data['chart']['result'][0]['indicators']['quote'][0]
                    
                    df = pd.DataFrame({
                        'Date': pd.to_datetime(timestamps, unit='s'),
                        'Open': quotes['open'],
                        'High': quotes['high'],
                        'Low': quotes['low'],
                        'Close': quotes['close'],
                        'Volume': quotes['volume']
                    })
                    df.set_index('Date', inplace=True)
                    return df
                else:
                    return pd.DataFrame()
        except Exception as e:
            print(f"Error in async fetch for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_sector_performance(self) -> pd.DataFrame:
        """Fetch sector performance data"""
        try:
            # Using SPDR sector ETFs as proxies
            sector_etfs = {
                'XLK': 'Technology',
                'XLV': 'Healthcare',
                'XLF': 'Financial Services',
                'XLY': 'Consumer Cyclical',
                'XLI': 'Industrials',
                'XLP': 'Consumer Defensive',
                'XLE': 'Energy',
                'XLB': 'Basic Materials',
                'XLRE': 'Real Estate',
                'XLC': 'Communication Services',
                'XLU': 'Utilities'
            }
            
            sector_data = {}
            for etf, sector in sector_etfs.items():
                data = self.get_stock_data(etf, period="6mo")
                if not data.empty:
                    sector_data[sector] = {
                        'etf': etf,
                        'current_price': data['Close'].iloc[-1],
                        'price_6mo_ago': data['Close'].iloc[0],
                        'return_6mo': (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100,
                        'volatility': data['Close'].pct_change().std() * np.sqrt(252) * 100
                    }
            
            return pd.DataFrame.from_dict(sector_data, orient='index')
        except Exception as e:
            print(f"Error fetching sector performance: {e}")
            return pd.DataFrame()
    
    def get_market_breadth(self) -> Dict:
        """Calculate market breadth indicators"""
        try:
            # Get S&P 500 components
            sp500 = yf.Ticker("^GSPC")
            sp500_data = sp500.history(period="1mo")
            
            # Calculate advance/decline ratio (simplified)
            up_days = len(sp500_data[sp500_data['Close'] > sp500_data['Open']])
            down_days = len(sp500_data[sp500_data['Close'] < sp500_data['Open']])
            
            return {
                'advance_decline_ratio': up_days / max(down_days, 1),
                'up_days': up_days,
                'down_days': down_days,
                'total_days': len(sp500_data)
            }
        except Exception as e:
            print(f"Error calculating market breadth: {e}")
            return {}