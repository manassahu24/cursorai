#!/usr/bin/env python3
"""
Test script for the Algorithmic Trading System
"""

import sys
import traceback
from trading_system import TradingSystem

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing Basic Functionality...")
    
    try:
        # Initialize system
        system = TradingSystem()
        print("✅ TradingSystem initialized successfully")
        
        # Test single stock analysis
        print("\n📊 Testing single stock analysis...")
        analysis = system.analyze_stock('AAPL')
        
        if analysis and analysis['overall_score'] > 0:
            print(f"✅ AAPL analysis successful - Score: {analysis['overall_score']:.1f}")
            print(f"   Recommendation: {analysis['recommendation']}")
            print(f"   Fundamental Score: {analysis['fundamental_score']:.1f}")
            print(f"   Technical Score: {analysis['technical_score']:.1f}")
        else:
            print("❌ AAPL analysis failed")
            return False
        
        # Test stock screening
        print("\n🔍 Testing stock screening...")
        test_stocks = ['AAPL', 'MSFT', 'GOOGL']
        screened = system.screen_stocks(test_stocks)
        
        if screened:
            print(f"✅ Stock screening successful - Found {len(screened)} stocks")
            for stock in screened:
                print(f"   {stock['symbol']}: {stock['overall_score']:.1f} score")
        else:
            print("❌ Stock screening failed")
            return False
        
        # Test sector analysis
        print("\n🏭 Testing sector analysis...")
        sectors = system.analyze_sector_performance()
        
        if sectors:
            print(f"✅ Sector analysis successful - Analyzed {len(sectors)} sectors")
            for sector, data in list(sectors.items())[:3]:  # Show first 3
                print(f"   {sector}: {data['return_6mo']:.1f}% return")
        else:
            print("❌ Sector analysis failed")
            return False
        
        # Test portfolio recommendations
        print("\n💼 Testing portfolio recommendations...")
        recommendations = system.generate_portfolio_recommendations(screened, sectors)
        
        if recommendations and 'sector_allocation' in recommendations:
            print("✅ Portfolio recommendations generated successfully")
            print(f"   Top stocks: {len(recommendations['top_stocks'])}")
            print(f"   Sectors analyzed: {len(recommendations['sector_allocation'])}")
        else:
            print("❌ Portfolio recommendations failed")
            return False
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        traceback.print_exc()
        return False

def test_data_fetching():
    """Test data fetching capabilities"""
    print("\n📡 Testing Data Fetching...")
    
    try:
        system = TradingSystem()
        
        # Test stock data fetching
        print("   Testing stock data fetching...")
        data = system.get_stock_data('AAPL', period="1mo")
        if not data.empty:
            print(f"   ✅ Stock data fetched - {len(data)} records")
        else:
            print("   ❌ Stock data fetching failed")
            return False
        
        # Test fundamental data fetching
        print("   Testing fundamental data fetching...")
        fundamental_data = system.get_fundamental_data('AAPL')
        if fundamental_data and 'market_cap' in fundamental_data:
            print(f"   ✅ Fundamental data fetched - Market Cap: ${fundamental_data['market_cap']:,.0f}")
        else:
            print("   ❌ Fundamental data fetching failed")
            return False
        
        # Test technical indicators
        print("   Testing technical indicators...")
        technical_data = system.calculate_technical_indicators(data)
        if not technical_data.empty and 'RSI' in technical_data.columns:
            print(f"   ✅ Technical indicators calculated - RSI: {technical_data['RSI'].iloc[-1]:.2f}")
        else:
            print("   ❌ Technical indicators calculation failed")
            return False
        
        print("   ✅ All data fetching tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Data fetching test failed: {e}")
        return False

def test_scoring_system():
    """Test the scoring system"""
    print("\n📊 Testing Scoring System...")
    
    try:
        system = TradingSystem()
        
        # Test fundamental scoring
        print("   Testing fundamental scoring...")
        test_fundamental_data = {
            'pe_ratio': 20.0,
            'price_to_book': 2.0,
            'debt_to_equity': 0.5,
            'current_ratio': 1.5,
            'roe': 0.15,
            'roa': 0.08,
            'profit_margins': 0.12,
            'revenue_growth': 0.10,
            'earnings_growth': 0.08,
            'beta': 1.0
        }
        
        fundamental_score, breakdown = system.fundamental_score(test_fundamental_data)
        if fundamental_score > 0:
            print(f"   ✅ Fundamental scoring works - Score: {fundamental_score:.1f}")
            print(f"      Breakdown: {list(breakdown.keys())}")
        else:
            print("   ❌ Fundamental scoring failed")
            return False
        
        # Test technical scoring
        print("   Testing technical scoring...")
        data = system.get_stock_data('AAPL', period="3mo")
        if not data.empty:
            technical_data = system.calculate_technical_indicators(data)
            technical_score, breakdown = system.technical_score(technical_data)
            if technical_score > 0:
                print(f"   ✅ Technical scoring works - Score: {technical_score:.1f}")
                print(f"      Breakdown: {list(breakdown.keys())}")
            else:
                print("   ❌ Technical scoring failed")
                return False
        else:
            print("   ❌ Could not fetch data for technical scoring test")
            return False
        
        print("   ✅ All scoring tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Scoring test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Algorithmic Trading System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_data_fetching,
        test_scoring_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo run the system:")
        print("  python main.py")
        print("\nTo launch the dashboard:")
        print("  streamlit run dashboard.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)