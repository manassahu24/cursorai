# Algorithmic Trading System

A comprehensive algorithmic trading system that performs fundamental and technical analysis on stocks, with sector analysis and rotation capabilities.

## 🚀 Features

### 📊 Fundamental Analysis
- **Financial Ratios**: PE, PB, Debt-to-Equity, Current Ratio, ROE, ROA
- **Growth Metrics**: Revenue growth, earnings growth
- **Profitability**: Profit margins, return metrics
- **Risk Assessment**: Beta, volatility analysis
- **Stock Screening**: Filter stocks based on fundamental criteria

### 📈 Technical Analysis
- **Moving Averages**: SMA, EMA with multiple timeframes
- **Momentum Indicators**: RSI, MACD, Stochastic Oscillator
- **Volatility Indicators**: Bollinger Bands, ATR
- **Volume Analysis**: OBV, Volume SMA
- **Pattern Recognition**: Support/Resistance, Chart patterns
- **Signal Generation**: Buy/Sell signals based on technical indicators

### 🏭 Sector Analysis
- **Sector Performance**: Track sector ETFs and performance
- **Sector Rotation**: Identify leading and lagging sectors
- **Correlation Analysis**: Sector correlations and diversification
- **Sector Allocation**: Optimal sector weight recommendations

### 💼 Portfolio Management
- **Risk Management**: Position sizing, stop-loss, take-profit
- **Portfolio Optimization**: Modern Portfolio Theory implementation
- **Rebalancing**: Automated rebalancing recommendations
- **Performance Tracking**: Portfolio performance metrics

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd algorithmic-trading-system
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional):
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

## 📖 Usage

### Basic Usage

```python
from trading_system import TradingSystem

# Initialize system
system = TradingSystem()

# Analyze a single stock
analysis = system.analyze_stock('AAPL')
print(analysis)

# Screen multiple stocks
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
screened = system.screen_stocks(stocks)
print(screened)

# Analyze sectors
sectors = system.analyze_sectors()
print(sectors)
```

### Command Line Usage

```bash
# Run the main analysis
python main.py

# Run the web dashboard
streamlit run dashboard.py
```

### Web Dashboard

The system includes a beautiful Streamlit dashboard with:

- **Interactive stock screening**
- **Real-time sector analysis**
- **Portfolio recommendations**
- **Individual stock analysis**
- **Visual charts and metrics**

To launch the dashboard:
```bash
streamlit run dashboard.py
```

## 📊 System Architecture

```
algorithmic-trading-system/
├── trading_system.py      # Main trading system class
├── main.py               # Command line interface
├── dashboard.py          # Streamlit web dashboard
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ⚙️ Configuration

### Fundamental Analysis Parameters
```python
min_market_cap = 1000000000  # $1B minimum
min_volume = 1000000         # 1M minimum volume
max_pe_ratio = 50           # Maximum PE ratio
min_pe_ratio = 5            # Minimum PE ratio
max_debt_to_equity = 2.0    # Maximum debt ratio
min_current_ratio = 1.0     # Minimum current ratio
min_roe = 0.10              # 10% minimum ROE
```

### Technical Analysis Parameters
```python
# Moving Averages
SMA_20 = 20
SMA_50 = 50

# RSI
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
```

## 📈 Scoring System

### Fundamental Score (0-100)
- **Valuation (25%)**: PE ratio, Price-to-Book ratio
- **Financial Health (25%)**: Debt-to-Equity, Current Ratio
- **Profitability (25%)**: ROE, ROA, Profit Margins
- **Growth (15%)**: Revenue growth, Earnings growth
- **Risk (10%)**: Beta analysis

### Technical Score (0-100)
- **Trend (30%)**: Moving average analysis, trend consistency
- **Momentum (25%)**: RSI, MACD analysis
- **Volatility (20%)**: Bollinger Bands, ATR analysis
- **Volume (15%)**: Volume trends, OBV analysis
- **Support/Resistance (10%)**: Price levels analysis

### Overall Score
```
Overall Score = (Fundamental Score × 0.6) + (Technical Score × 0.4)
```

## 🏭 Sector Analysis

The system analyzes 11 major sectors using SPDR ETFs:

| Sector | ETF | Description |
|--------|-----|-------------|
| Technology | XLK | Software, hardware, semiconductors |
| Healthcare | XLV | Pharmaceuticals, biotech, medical devices |
| Financial Services | XLF | Banks, insurance, financial services |
| Consumer Cyclical | XLY | Retail, automotive, travel |
| Industrials | XLI | Manufacturing, aerospace, defense |
| Consumer Defensive | XLP | Food, beverages, household products |
| Energy | XLE | Oil, gas, renewable energy |
| Basic Materials | XLB | Chemicals, metals, mining |
| Real Estate | XLRE | REITs, real estate services |
| Communication Services | XLC | Media, telecom, internet |
| Utilities | XLU | Electric, gas, water utilities |

## 📊 Trading Signals

### Buy Signals
- RSI oversold (< 30)
- MACD crossover above signal line
- Price near Bollinger Band support
- Golden cross (SMA crossover)
- Volume spike with price increase

### Sell Signals
- RSI overbought (> 70)
- MACD crossover below signal line
- Price near Bollinger Band resistance
- Death cross (SMA crossover)
- Volume spike with price decrease

## 💼 Portfolio Recommendations

The system provides:

1. **Top Stock Picks**: Highest-scoring stocks meeting criteria
2. **Sector Allocation**: Optimal sector weights based on performance
3. **Risk Assessment**: Portfolio beta and risk level
4. **Rebalancing Suggestions**: When to adjust positions

## 🔧 Customization

### Adding New Indicators

```python
def custom_indicator(self, data):
    # Your custom indicator logic
    return indicator_value

# Add to technical_score method
custom_score = self.custom_indicator(data) * weight
```

### Modifying Scoring Weights

```python
# In fundamental_score method
weights = {
    'valuation': 0.30,      # Increase valuation weight
    'financial_health': 0.20,
    'profitability': 0.25,
    'growth': 0.15,
    'risk': 0.10
}
```

### Custom Stock Universe

```python
# Add your own stock list
custom_stocks = ['YOUR_STOCK1', 'YOUR_STOCK2', 'YOUR_STOCK3']
screened = system.screen_stocks(custom_stocks)
```

## 📊 Data Sources

- **Yahoo Finance**: Primary data source for stock prices and fundamentals
- **Real-time data**: Live market data and indicators
- **Historical data**: 1-year historical data for analysis

## 🧪 Testing

Run the system with sample data:

```bash
python main.py
```

This will:
1. Analyze a predefined list of stocks
2. Display top performers
3. Show sector analysis
4. Generate portfolio recommendations

## 📈 Example Output

```
🚀 Starting Algorithmic Trading System...
============================================================
📊 Analyzing 35 stocks...
------------------------------------------------------------
✅ Found 12 stocks meeting criteria

🏆 TOP 10 STOCKS
------------------------------------------------------------
 1. AAPL   | Score:  85.2 | Fund:  88.5 | Tech:  80.1 | STRONG_BUY | Technology
 2. MSFT   | Score:  82.1 | Fund:  85.2 | Tech:  77.8 | STRONG_BUY | Technology
 3. GOOGL  | Score:  78.9 | Fund:  82.1 | Tech:  74.5 | BUY       | Technology
 4. AMZN   | Score:  75.4 | Fund:  78.9 | Tech:  70.8 | BUY       | Consumer Cyclical
 5. TSLA   | Score:  72.8 | Fund:  75.4 | Tech:  69.2 | BUY       | Consumer Cyclical

📈 SECTOR ANALYSIS
------------------------------------------------------------
 1. Technology           | ETF: XLK  | Return:  15.2% | Vol: 18.5% | Tech Score: 82.1 | Momentum: 95.3
 2. Healthcare           | ETF: XLV  | Return:   8.7% | Vol: 15.2% | Tech Score: 75.4 | Momentum: 52.1
 3. Financial Services   | ETF: XLF  | Return:   5.1% | Vol: 12.8% | Tech Score: 68.9 | Momentum: 37.8
```

## ⚠️ Disclaimer

This software is for **educational and research purposes only**. It is not intended to provide financial advice. Always do your own research and consult with a financial advisor before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the example code

## 🚀 Roadmap

- [ ] Machine learning integration
- [ ] Real-time data streaming
- [ ] Advanced pattern recognition
- [ ] Options analysis
- [ ] Cryptocurrency support
- [ ] Backtesting framework
- [ ] Paper trading mode
- [ ] Mobile app
- [ ] Social sentiment analysis
- [ ] ESG scoring integration

## 📊 Performance Metrics

The system tracks various performance metrics:

### Fundamental Metrics
- Fundamental Score (0-100)
- Valuation Score
- Financial Health Score
- Profitability Score
- Growth Score
- Risk Score

### Technical Metrics
- Technical Score (0-100)
- Trend Score
- Momentum Score
- Volatility Score
- Volume Score
- Support/Resistance Score

### Portfolio Metrics
- Sharpe Ratio
- Maximum Drawdown
- Beta
- Alpha
- Information Ratio
- Sortino Ratio

---

**Happy Trading! 📈💰**