#!/usr/bin/env python3
"""
Main script to run the Algorithmic Trading System
Demonstrates fundamental and technical analysis with sector rotation
"""

from trading_system import TradingSystem
import pandas as pd
from datetime import datetime

def main():
    print("🚀 Starting Algorithmic Trading System...")
    print("=" * 60)
    
    # Initialize the trading system
    system = TradingSystem()
    
    # Sample stock universe (you can expand this list)
    sample_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
        'JPM', 'JNJ', 'PG', 'UNH', 'HD', 'MA', 'V', 'PYPL', 'ADBE', 'CRM',
        'NKE', 'DIS', 'WMT', 'KO', 'PEP', 'ABT', 'TMO', 'AVGO', 'COST',
        'ACN', 'DHR', 'LLY', 'MRK', 'PFE', 'TXN', 'UNP', 'UPS', 'RTX'
    ]
    
    print(f"📊 Analyzing {len(sample_stocks)} stocks...")
    print("-" * 60)
    
    # Screen stocks based on fundamental and technical criteria
    screened_stocks = system.screen_stocks(sample_stocks)
    
    print(f"✅ Found {len(screened_stocks)} stocks meeting criteria")
    print()
    
    # Display top 10 stocks
    print("🏆 TOP 10 STOCKS")
    print("-" * 60)
    for i, stock in enumerate(screened_stocks[:10], 1):
        symbol = stock['symbol']
        overall_score = stock['overall_score']
        fundamental_score = stock['fundamental_score']
        technical_score = stock['technical_score']
        recommendation = stock['recommendation']
        sector = stock['fundamental_data'].get('sector', 'Unknown')
        
        print(f"{i:2d}. {symbol:6s} | Score: {overall_score:5.1f} | "
              f"Fund: {fundamental_score:5.1f} | Tech: {technical_score:5.1f} | "
              f"{recommendation:10s} | {sector}")
    
    print()
    
    # Analyze sector performance
    print("📈 SECTOR ANALYSIS")
    print("-" * 60)
    sector_analysis = system.analyze_sector_performance()
    
    # Sort sectors by performance
    sorted_sectors = sorted(sector_analysis.items(), 
                          key=lambda x: x[1]['momentum'], reverse=True)
    
    for i, (sector, data) in enumerate(sorted_sectors, 1):
        etf = data['etf']
        return_6mo = data['return_6mo']
        volatility = data['volatility']
        technical_score = data['technical_score']
        momentum = data['momentum']
        
        print(f"{i:2d}. {sector:20s} | ETF: {etf:4s} | "
              f"Return: {return_6mo:6.1f}% | Vol: {volatility:5.1f}% | "
              f"Tech Score: {technical_score:5.1f} | Momentum: {momentum:6.1f}")
    
    print()
    
    # Generate portfolio recommendations
    print("💼 PORTFOLIO RECOMMENDATIONS")
    print("-" * 60)
    recommendations = system.generate_portfolio_recommendations(screened_stocks, sector_analysis)
    
    # Display sector allocation
    print("Sector Allocation:")
    for sector, weight in recommendations['sector_allocation'].items():
        print(f"  {sector:20s}: {weight:.1%}")
    
    print()
    
    # Display risk assessment
    if recommendations['risk_assessment']:
        risk_data = recommendations['risk_assessment']
        print(f"Risk Assessment:")
        print(f"  Portfolio Beta: {risk_data['portfolio_beta']:.2f}")
        print(f"  Risk Level: {risk_data['risk_level']}")
    
    print()
    
    # Show detailed analysis for top 3 stocks
    print("🔍 DETAILED ANALYSIS - TOP 3 STOCKS")
    print("=" * 60)
    
    for i, stock in enumerate(screened_stocks[:3], 1):
        print(f"\n{i}. {stock['symbol']} - {stock['recommendation']}")
        print("-" * 40)
        
        # Fundamental breakdown
        if 'fundamental_breakdown' in stock:
            print("Fundamental Breakdown:")
            for category, score in stock['fundamental_breakdown'].items():
                print(f"  {category.replace('_', ' ').title()}: {score:.1f}")
        
        # Technical breakdown
        if 'technical_breakdown' in stock:
            print("Technical Breakdown:")
            for category, score in stock['technical_breakdown'].items():
                print(f"  {category.replace('_', ' ').title()}: {score:.1f}")
        
        # Trading signals
        if stock['signals']:
            print("Trading Signals:")
            for signal in stock['signals']:
                print(f"  {signal['type']} - {signal['indicator']} ({signal['strength']})")
                print(f"    Reason: {signal['reason']}")
        else:
            print("Trading Signals: None")
    
    print()
    print("=" * 60)
    print("✅ Analysis Complete!")
    print(f"📅 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        'screened_stocks': screened_stocks,
        'sector_analysis': sector_analysis,
        'recommendations': recommendations
    }

def analyze_single_stock(symbol: str):
    """Analyze a single stock in detail"""
    print(f"🔍 Analyzing {symbol}...")
    print("=" * 50)
    
    system = TradingSystem()
    analysis = system.analyze_stock(symbol)
    
    if analysis['overall_score'] > 0:
        print(f"Symbol: {analysis['symbol']}")
        print(f"Overall Score: {analysis['overall_score']:.1f}/100")
        print(f"Fundamental Score: {analysis['fundamental_score']:.1f}/100")
        print(f"Technical Score: {analysis['technical_score']:.1f}/100")
        print(f"Recommendation: {analysis['recommendation']}")
        print(f"Sector: {analysis['fundamental_data'].get('sector', 'Unknown')}")
        
        print("\nFundamental Data:")
        fundamental_data = analysis['fundamental_data']
        if fundamental_data:
            print(f"  Market Cap: ${fundamental_data.get('market_cap', 0):,.0f}")
            print(f"  PE Ratio: {fundamental_data.get('pe_ratio', 0):.2f}")
            print(f"  ROE: {fundamental_data.get('roe', 0):.2%}")
            print(f"  Debt/Equity: {fundamental_data.get('debt_to_equity', 0):.2f}")
            print(f"  Current Ratio: {fundamental_data.get('current_ratio', 0):.2f}")
        
        print("\nTrading Signals:")
        for signal in analysis['signals']:
            print(f"  {signal['type']} - {signal['indicator']} ({signal['strength']})")
            print(f"    {signal['reason']}")
    else:
        print(f"❌ Unable to analyze {symbol}")

if __name__ == "__main__":
    # Run the main analysis
    results = main()
    
    # Example: Analyze a specific stock
    print("\n" + "=" * 60)
    analyze_single_stock('AAPL')