import yfinance as yf
import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class TradingSystem:
    def __init__(self):
        # Configuration parameters
        self.min_market_cap = 1000000000  # $1B minimum
        self.min_volume = 1000000  # 1M minimum volume
        self.max_pe_ratio = 50
        self.min_pe_ratio = 5
        self.max_debt_to_equity = 2.0
        self.min_current_ratio = 1.0
        self.min_roe = 0.10
        
        # Sectors to analyze
        self.sectors = [
            'Technology', 'Healthcare', 'Financial Services', 'Consumer Cyclical',
            'Industrials', 'Consumer Defensive', 'Energy', 'Basic Materials',
            'Real Estate', 'Communication Services', 'Utilities'
        ]
        
        # Sector ETFs for analysis
        self.sector_etfs = {
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
            
            return {
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
        except Exception as e:
            print(f"Error fetching fundamental data for {symbol}: {e}")
            return {}
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        if data.empty:
            return data
            
        df = data.copy()
        
        try:
            # Moving Averages
            df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
            df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
            df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
            
            # RSI
            df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
            
            # MACD
            macd = ta.trend.MACD(df['Close'])
            df['MACD'] = macd.macd()
            df['MACD_Signal'] = macd.macd_signal()
            df['MACD_Histogram'] = macd.macd_diff()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['Close'])
            df['BB_Upper'] = bb.bollinger_hband()
            df['BB_Lower'] = bb.bollinger_lband()
            df['BB_Middle'] = bb.bollinger_mavg()
            df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
            df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
            
            # Volume Indicators
            df['Volume_SMA'] = ta.volume.volume_sma(df['Close'], df['Volume'])
            df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
            
            # ATR for volatility
            df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
            
        except Exception as e:
            print(f"Error calculating technical indicators: {e}")
            
        return df
    
    def fundamental_score(self, fundamental_data: Dict) -> Tuple[float, Dict]:
        """Calculate fundamental score (0-100) with breakdown"""
        score = 0
        weights = {
            'valuation': 0.25,
            'financial_health': 0.25,
            'profitability': 0.25,
            'growth': 0.15,
            'risk': 0.10
        }
        
        scores = {}
        
        try:
            # Valuation Score (0-25 points)
            pe_score = self._score_pe_ratio(fundamental_data.get('pe_ratio', 0))
            pb_score = self._score_price_to_book(fundamental_data.get('price_to_book', 0))
            valuation_score = (pe_score + pb_score) / 2 * weights['valuation']
            scores['valuation'] = valuation_score
            score += valuation_score
            
            # Financial Health Score (0-25 points)
            debt_score = self._score_debt_to_equity(fundamental_data.get('debt_to_equity', 0))
            current_ratio_score = self._score_current_ratio(fundamental_data.get('current_ratio', 0))
            health_score = (debt_score + current_ratio_score) / 2 * weights['financial_health']
            scores['financial_health'] = health_score
            score += health_score
            
            # Profitability Score (0-25 points)
            roe_score = self._score_roe(fundamental_data.get('roe', 0))
            roa_score = self._score_roa(fundamental_data.get('roa', 0))
            margin_score = self._score_profit_margin(fundamental_data.get('profit_margins', 0))
            profitability_score = (roe_score + roa_score + margin_score) / 3 * weights['profitability']
            scores['profitability'] = profitability_score
            score += profitability_score
            
            # Growth Score (0-15 points)
            revenue_growth_score = self._score_growth(fundamental_data.get('revenue_growth', 0))
            earnings_growth_score = self._score_growth(fundamental_data.get('earnings_growth', 0))
            growth_score = (revenue_growth_score + earnings_growth_score) / 2 * weights['growth']
            scores['growth'] = growth_score
            score += growth_score
            
            # Risk Score (0-10 points)
            beta_score = self._score_beta(fundamental_data.get('beta', 0))
            risk_score = beta_score * weights['risk']
            scores['risk'] = risk_score
            score += risk_score
            
        except Exception as e:
            print(f"Error calculating fundamental score: {e}")
            
        return min(score, 100), scores
    
    def _score_pe_ratio(self, pe_ratio: float) -> float:
        """Score PE ratio (lower is better, but not too low)"""
        if pe_ratio <= 0 or pe_ratio > 100:
            return 0
        elif pe_ratio <= 15:
            return 100
        elif pe_ratio <= 25:
            return 80
        elif pe_ratio <= 35:
            return 60
        elif pe_ratio <= 50:
            return 40
        else:
            return 20
    
    def _score_price_to_book(self, pb_ratio: float) -> float:
        """Score Price-to-Book ratio"""
        if pb_ratio <= 0 or pb_ratio > 10:
            return 0
        elif pb_ratio <= 1:
            return 100
        elif pb_ratio <= 2:
            return 80
        elif pb_ratio <= 3:
            return 60
        elif pb_ratio <= 5:
            return 40
        else:
            return 20
    
    def _score_debt_to_equity(self, debt_equity: float) -> float:
        """Score Debt-to-Equity ratio (lower is better)"""
        if debt_equity < 0:
            return 0
        elif debt_equity <= 0.3:
            return 100
        elif debt_equity <= 0.5:
            return 80
        elif debt_equity <= 1.0:
            return 60
        elif debt_equity <= 2.0:
            return 40
        else:
            return 20
    
    def _score_current_ratio(self, current_ratio: float) -> float:
        """Score Current Ratio"""
        if current_ratio <= 0:
            return 0
        elif current_ratio >= 2.0:
            return 100
        elif current_ratio >= 1.5:
            return 80
        elif current_ratio >= 1.0:
            return 60
        else:
            return 20
    
    def _score_roe(self, roe: float) -> float:
        """Score Return on Equity"""
        if roe <= 0:
            return 0
        elif roe >= 0.20:
            return 100
        elif roe >= 0.15:
            return 80
        elif roe >= 0.10:
            return 60
        elif roe >= 0.05:
            return 40
        else:
            return 20
    
    def _score_roa(self, roa: float) -> float:
        """Score Return on Assets"""
        if roa <= 0:
            return 0
        elif roa >= 0.10:
            return 100
        elif roa >= 0.07:
            return 80
        elif roa >= 0.05:
            return 60
        elif roa >= 0.03:
            return 40
        else:
            return 20
    
    def _score_profit_margin(self, margin: float) -> float:
        """Score Profit Margin"""
        if margin <= 0:
            return 0
        elif margin >= 0.20:
            return 100
        elif margin >= 0.15:
            return 80
        elif margin >= 0.10:
            return 60
        elif margin >= 0.05:
            return 40
        else:
            return 20
    
    def _score_growth(self, growth_rate: float) -> float:
        """Score Growth Rate"""
        if growth_rate <= 0:
            return 0
        elif growth_rate >= 0.20:
            return 100
        elif growth_rate >= 0.15:
            return 80
        elif growth_rate >= 0.10:
            return 60
        elif growth_rate >= 0.05:
            return 40
        else:
            return 20
    
    def _score_beta(self, beta: float) -> float:
        """Score Beta (prefer moderate beta)"""
        if beta <= 0:
            return 50
        elif 0.8 <= beta <= 1.2:
            return 100
        elif 0.6 <= beta <= 1.4:
            return 80
        elif 0.4 <= beta <= 1.6:
            return 60
        else:
            return 40
    
    def technical_score(self, data: pd.DataFrame) -> Tuple[float, Dict]:
        """Calculate technical score (0-100) with breakdown"""
        if data.empty or len(data) < 50:
            return 0, {}
            
        score = 0
        weights = {
            'trend': 0.30,
            'momentum': 0.25,
            'volatility': 0.20,
            'volume': 0.15,
            'support_resistance': 0.10
        }
        
        scores = {}
        
        try:
            # Trend Score (0-30 points)
            trend_score = self._calculate_trend_score(data) * weights['trend']
            scores['trend'] = trend_score
            score += trend_score
            
            # Momentum Score (0-25 points)
            momentum_score = self._calculate_momentum_score(data) * weights['momentum']
            scores['momentum'] = momentum_score
            score += momentum_score
            
            # Volatility Score (0-20 points)
            volatility_score = self._calculate_volatility_score(data) * weights['volatility']
            scores['volatility'] = volatility_score
            score += volatility_score
            
            # Volume Score (0-15 points)
            volume_score = self._calculate_volume_score(data) * weights['volume']
            scores['volume'] = volume_score
            score += volume_score
            
            # Support/Resistance Score (0-10 points)
            sr_score = self._calculate_support_resistance_score(data) * weights['support_resistance']
            scores['support_resistance'] = sr_score
            score += sr_score
            
        except Exception as e:
            print(f"Error calculating technical score: {e}")
            
        return min(score, 100), scores
    
    def _calculate_trend_score(self, data: pd.DataFrame) -> float:
        """Calculate trend strength score"""
        if len(data) < 50:
            return 0
            
        current_price = data['Close'].iloc[-1]
        sma_20 = data['SMA_20'].iloc[-1]
        sma_50 = data['SMA_50'].iloc[-1]
        
        score = 0
        
        # Price vs moving averages
        if current_price > sma_20:
            score += 20
        if current_price > sma_50:
            score += 20
        if sma_20 > sma_50:
            score += 20
            
        # Trend consistency
        recent_trend = (data['Close'].iloc[-5:] > data['Close'].iloc[-10:-5]).sum()
        score += (recent_trend / 5) * 40
            
        return score
    
    def _calculate_momentum_score(self, data: pd.DataFrame) -> float:
        """Calculate momentum score"""
        if len(data) < 14:
            return 0
            
        rsi = data['RSI'].iloc[-1]
        macd = data['MACD'].iloc[-1]
        macd_signal = data['MACD_Signal'].iloc[-1]
        
        score = 0
        
        # RSI analysis
        if 30 <= rsi <= 70:
            score += 25
        elif rsi < 30:  # Oversold
            score += 15
        elif rsi > 70:  # Overbought
            score += 10
            
        # MACD analysis
        if macd > macd_signal:
            score += 25
        if macd > 0:
            score += 25
            
        return score
    
    def _calculate_volatility_score(self, data: pd.DataFrame) -> float:
        """Calculate volatility score"""
        if len(data) < 14:
            return 0
            
        bb_position = data['BB_Position'].iloc[-1]
        atr = data['ATR'].iloc[-1]
        avg_atr = data['ATR'].rolling(14).mean().iloc[-1]
        
        score = 0
        
        # Bollinger Band position
        if 0.2 <= bb_position <= 0.8:
            score += 50
        elif bb_position < 0.2:  # Near support
            score += 30
        elif bb_position > 0.8:  # Near resistance
            score += 20
            
        # ATR analysis (moderate volatility preferred)
        if 0.5 <= (atr / avg_atr) <= 1.5:
            score += 50
        else:
            score += 25
            
        return score
    
    def _calculate_volume_score(self, data: pd.DataFrame) -> float:
        """Calculate volume score"""
        if len(data) < 20:
            return 0
            
        current_volume = data['Volume'].iloc[-1]
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
        obv_trend = data['OBV'].iloc[-5:].pct_change().mean()
        
        score = 0
        
        # Volume vs average
        if current_volume > avg_volume * 1.2:
            score += 50
        elif current_volume > avg_volume:
            score += 30
        else:
            score += 10
            
        # OBV trend
        if obv_trend > 0:
            score += 50
        else:
            score += 20
            
        return score
    
    def _calculate_support_resistance_score(self, data: pd.DataFrame) -> float:
        """Calculate support/resistance score"""
        if len(data) < 20:
            return 0
            
        current_price = data['Close'].iloc[-1]
        recent_low = data['Low'].iloc[-20:].min()
        recent_high = data['High'].iloc[-20:].max()
        
        score = 0
        
        # Distance from support/resistance
        support_distance = (current_price - recent_low) / current_price
        resistance_distance = (recent_high - current_price) / current_price
        
        if support_distance < 0.05:  # Near support
            score += 50
        elif resistance_distance < 0.05:  # Near resistance
            score += 30
        else:
            score += 20
            
        return score
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Complete analysis of a stock"""
        analysis = {
            'symbol': symbol,
            'fundamental_data': {},
            'technical_data': {},
            'fundamental_score': 0,
            'technical_score': 0,
            'overall_score': 0,
            'recommendation': 'HOLD',
            'signals': []
        }
        
        try:
            # Get fundamental data
            fundamental_data = self.get_fundamental_data(symbol)
            analysis['fundamental_data'] = fundamental_data
            
            # Get technical data
            stock_data = self.get_stock_data(symbol)
            if not stock_data.empty:
                technical_data = self.calculate_technical_indicators(stock_data)
                analysis['technical_data'] = technical_data
                
                # Calculate scores
                fundamental_score, fundamental_breakdown = self.fundamental_score(fundamental_data)
                technical_score, technical_breakdown = self.technical_score(technical_data)
                
                analysis['fundamental_score'] = fundamental_score
                analysis['technical_score'] = technical_score
                analysis['overall_score'] = (fundamental_score * 0.6) + (technical_score * 0.4)
                analysis['fundamental_breakdown'] = fundamental_breakdown
                analysis['technical_breakdown'] = technical_breakdown
                
                # Generate recommendation
                if analysis['overall_score'] >= 80:
                    analysis['recommendation'] = 'STRONG_BUY'
                elif analysis['overall_score'] >= 70:
                    analysis['recommendation'] = 'BUY'
                elif analysis['overall_score'] >= 50:
                    analysis['recommendation'] = 'HOLD'
                elif analysis['overall_score'] >= 30:
                    analysis['recommendation'] = 'SELL'
                else:
                    analysis['recommendation'] = 'STRONG_SELL'
                
                # Generate trading signals
                analysis['signals'] = self.generate_signals(technical_data)
                    
        except Exception as e:
            print(f"Error analyzing stock {symbol}: {e}")
            
        return analysis
    
    def generate_signals(self, data: pd.DataFrame) -> List[Dict]:
        """Generate trading signals based on technical analysis"""
        signals = []
        
        if data.empty or len(data) < 50:
            return signals
            
        try:
            current_price = data['Close'].iloc[-1]
            rsi = data['RSI'].iloc[-1]
            macd = data['MACD'].iloc[-1]
            macd_signal = data['MACD_Signal'].iloc[-1]
            bb_position = data['BB_Position'].iloc[-1]
            
            # RSI signals
            if rsi < 30:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'RSI',
                    'strength': 'Strong',
                    'reason': 'Oversold condition'
                })
            elif rsi > 70:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'RSI',
                    'strength': 'Strong',
                    'reason': 'Overbought condition'
                })
                
            # MACD signals
            if macd > macd_signal and macd < 0:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'MACD',
                    'strength': 'Medium',
                    'reason': 'MACD crossover above signal line'
                })
            elif macd < macd_signal and macd > 0:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'MACD',
                    'strength': 'Medium',
                    'reason': 'MACD crossover below signal line'
                })
                
            # Bollinger Band signals
            if bb_position < 0.2:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'Bollinger Bands',
                    'strength': 'Medium',
                    'reason': 'Price near lower band'
                })
            elif bb_position > 0.8:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'Bollinger Bands',
                    'strength': 'Medium',
                    'reason': 'Price near upper band'
                })
                
        except Exception as e:
            print(f"Error generating signals: {e}")
            
        return signals
    
    def screen_stocks(self, symbols: List[str]) -> List[Dict]:
        """Screen multiple stocks and return top performers"""
        screened_stocks = []
        
        for symbol in symbols:
            try:
                analysis = self.analyze_stock(symbol)
                
                # Apply filters
                fundamental_data = analysis['fundamental_data']
                if (fundamental_data.get('market_cap', 0) >= self.min_market_cap and
                    fundamental_data.get('volume', 0) >= self.min_volume and
                    analysis['overall_score'] >= 60):
                    screened_stocks.append(analysis)
                    
            except Exception as e:
                print(f"Error screening {symbol}: {e}")
                continue
        
        # Sort by overall score
        screened_stocks.sort(key=lambda x: x['overall_score'], reverse=True)
        return screened_stocks
    
    def analyze_sector_performance(self) -> Dict:
        """Analyze sector performance using sector ETFs"""
        sector_analysis = {}
        
        for etf, sector in self.sector_etfs.items():
            try:
                data = self.get_stock_data(etf, period="6mo")
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    price_6mo_ago = data['Close'].iloc[0]
                    return_6mo = (current_price / price_6mo_ago - 1) * 100
                    volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
                    
                    # Calculate technical indicators for sector
                    technical_data = self.calculate_technical_indicators(data)
                    technical_score, _ = self.technical_score(technical_data)
                    
                    sector_analysis[sector] = {
                        'etf': etf,
                        'current_price': current_price,
                        'return_6mo': return_6mo,
                        'volatility': volatility,
                        'technical_score': technical_score,
                        'momentum': return_6mo + technical_score * 0.5
                    }
            except Exception as e:
                print(f"Error analyzing sector {sector}: {e}")
        
        return sector_analysis
    
    def generate_portfolio_recommendations(self, top_stocks: List[Dict], sector_analysis: Dict) -> Dict:
        """Generate portfolio recommendations based on stock and sector analysis"""
        recommendations = {
            'top_stocks': top_stocks[:10],  # Top 10 stocks
            'sector_allocation': {},
            'risk_assessment': {},
            'rebalancing_suggestions': []
        }
        
        # Sector allocation based on performance
        sector_scores = {}
        for sector, data in sector_analysis.items():
            sector_scores[sector] = data['momentum']
        
        # Sort sectors by performance
        sorted_sectors = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Allocate more weight to top-performing sectors
        total_weight = 0
        for i, (sector, score) in enumerate(sorted_sectors):
            weight = max(0.05, 0.15 - i * 0.01)  # 15% to 5% allocation
            recommendations['sector_allocation'][sector] = weight
            total_weight += weight
        
        # Normalize weights
        for sector in recommendations['sector_allocation']:
            recommendations['sector_allocation'][sector] /= total_weight
        
        # Risk assessment
        if top_stocks:
            avg_beta = np.mean([stock['fundamental_data'].get('beta', 1.0) for stock in top_stocks[:10]])
            recommendations['risk_assessment'] = {
                'portfolio_beta': avg_beta,
                'risk_level': 'Moderate' if 0.8 <= avg_beta <= 1.2 else 'High' if avg_beta > 1.2 else 'Low'
            }
        
        return recommendations