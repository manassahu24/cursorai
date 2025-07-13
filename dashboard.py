import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from trading_system import TradingSystem
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Algorithmic Trading System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize trading system
@st.cache_resource
def get_trading_system():
    return TradingSystem()

def main():
    st.title("📈 Algorithmic Trading System")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("Settings")
    
    # Stock universe selection
    st.sidebar.subheader("Stock Universe")
    universe_options = {
        "Tech Giants": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'],
        "Blue Chips": ['JPM', 'JNJ', 'PG', 'UNH', 'HD', 'MA', 'V', 'PYPL'],
        "Growth Stocks": ['ADBE', 'CRM', 'NKE', 'DIS', 'WMT', 'KO', 'PEP'],
        "Healthcare": ['ABT', 'TMO', 'LLY', 'MRK', 'PFE', 'UNH', 'JNJ'],
        "Custom": []
    }
    
    selected_universe = st.sidebar.selectbox(
        "Select Stock Universe",
        list(universe_options.keys())
    )
    
    if selected_universe == "Custom":
        custom_stocks = st.sidebar.text_area(
            "Enter stock symbols (one per line)",
            value="AAPL\nMSFT\nGOOGL\nAMZN\nTSLA"
        )
        stock_list = [s.strip().upper() for s in custom_stocks.split('\n') if s.strip()]
    else:
        stock_list = universe_options[selected_universe]
    
    # Analysis parameters
    st.sidebar.subheader("Analysis Parameters")
    min_score = st.sidebar.slider("Minimum Overall Score", 0, 100, 60)
    min_market_cap = st.sidebar.number_input("Minimum Market Cap ($B)", 1, 100, 10) * 1e9
    
    # Run analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing stocks..."):
            system = get_trading_system()
            
            # Update system parameters
            system.min_market_cap = min_market_cap
            
            # Run analysis
            screened_stocks = system.screen_stocks(stock_list)
            sector_analysis = system.analyze_sector_performance()
            recommendations = system.generate_portfolio_recommendations(screened_stocks, sector_analysis)
            
            # Filter by minimum score
            screened_stocks = [s for s in screened_stocks if s['overall_score'] >= min_score]
            
            # Store results in session state
            st.session_state.screened_stocks = screened_stocks
            st.session_state.sector_analysis = sector_analysis
            st.session_state.recommendations = recommendations
    
    # Main content
    if 'screened_stocks' in st.session_state:
        display_results()
    else:
        st.info("👈 Use the sidebar to configure analysis parameters and click 'Run Analysis' to start.")
        
        # Show sample data
        st.subheader("📊 Sample Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Stocks by Score**")
            sample_data = pd.DataFrame({
                'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                'Score': [85.2, 82.1, 78.9, 75.4, 72.8],
                'Recommendation': ['STRONG_BUY', 'STRONG_BUY', 'BUY', 'BUY', 'BUY']
            })
            st.dataframe(sample_data, use_container_width=True)
        
        with col2:
            st.markdown("**Sector Performance**")
            sector_data = pd.DataFrame({
                'Sector': ['Technology', 'Healthcare', 'Financial', 'Consumer'],
                'Return (%)': [12.5, 8.2, 5.1, 3.8],
                'Volatility (%)': [18.2, 15.1, 12.8, 11.5]
            })
            st.dataframe(sector_data, use_container_width=True)

def display_results():
    screened_stocks = st.session_state.screened_stocks
    sector_analysis = st.session_state.sector_analysis
    recommendations = st.session_state.recommendations
    
    # Overview metrics
    st.subheader("📊 Analysis Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Stocks Analyzed", len(screened_stocks))
    
    with col2:
        avg_score = np.mean([s['overall_score'] for s in screened_stocks]) if screened_stocks else 0
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        strong_buys = len([s for s in screened_stocks if s['recommendation'] == 'STRONG_BUY'])
        st.metric("Strong Buys", strong_buys)
    
    with col4:
        if recommendations['risk_assessment']:
            risk_level = recommendations['risk_assessment']['risk_level']
            st.metric("Risk Level", risk_level)
    
    st.markdown("---")
    
    # Top stocks table
    st.subheader("🏆 Top Stocks")
    
    if screened_stocks:
        # Create DataFrame for display
        df_stocks = pd.DataFrame([
            {
                'Symbol': s['symbol'],
                'Overall Score': s['overall_score'],
                'Fundamental Score': s['fundamental_score'],
                'Technical Score': s['technical_score'],
                'Recommendation': s['recommendation'],
                'Sector': s['fundamental_data'].get('sector', 'Unknown'),
                'Market Cap ($B)': s['fundamental_data'].get('market_cap', 0) / 1e9,
                'PE Ratio': s['fundamental_data'].get('pe_ratio', 0),
                'ROE (%)': s['fundamental_data'].get('roe', 0) * 100
            }
            for s in screened_stocks
        ])
        
        # Color code recommendations
        def color_recommendation(val):
            if val == 'STRONG_BUY':
                return 'background-color: #90EE90'
            elif val == 'BUY':
                return 'background-color: #98FB98'
            elif val == 'SELL':
                return 'background-color: #FFB6C1'
            elif val == 'STRONG_SELL':
                return 'background-color: #FF69B4'
            else:
                return 'background-color: #F0F0F0'
        
        styled_df = df_stocks.style.applymap(color_recommendation, subset=['Recommendation'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Score distribution chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_scores = px.bar(
                df_stocks.head(10),
                x='Symbol',
                y='Overall Score',
                title="Top 10 Stocks by Overall Score",
                color='Overall Score',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_scores, use_container_width=True)
        
        with col2:
            fig_breakdown = go.Figure()
            
            symbols = df_stocks['Symbol'].head(10)
            fundamental_scores = df_stocks['Fundamental Score'].head(10)
            technical_scores = df_stocks['Technical Score'].head(10)
            
            fig_breakdown.add_trace(go.Bar(
                name='Fundamental',
                x=symbols,
                y=fundamental_scores,
                marker_color='blue'
            ))
            
            fig_breakdown.add_trace(go.Bar(
                name='Technical',
                x=symbols,
                y=technical_scores,
                marker_color='orange'
            ))
            
            fig_breakdown.update_layout(
                title="Score Breakdown - Top 10 Stocks",
                barmode='group',
                xaxis_title="Symbol",
                yaxis_title="Score"
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
    
    st.markdown("---")
    
    # Sector analysis
    st.subheader("📈 Sector Analysis")
    
    if sector_analysis:
        # Create DataFrame for sectors
        df_sectors = pd.DataFrame([
            {
                'Sector': sector,
                'ETF': data['etf'],
                '6-Month Return (%)': data['return_6mo'],
                'Volatility (%)': data['volatility'],
                'Technical Score': data['technical_score'],
                'Momentum': data['momentum']
            }
            for sector, data in sector_analysis.items()
        ])
        
        # Sort by momentum
        df_sectors = df_sectors.sort_values('Momentum', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(df_sectors, use_container_width=True)
        
        with col2:
            fig_sectors = px.bar(
                df_sectors,
                x='Sector',
                y='6-Month Return (%)',
                title="Sector Performance (6-Month Return)",
                color='6-Month Return (%)',
                color_continuous_scale='RdYlGn'
            )
            fig_sectors.update_xaxes(tickangle=45)
            st.plotly_chart(fig_sectors, use_container_width=True)
    
    st.markdown("---")
    
    # Portfolio recommendations
    st.subheader("💼 Portfolio Recommendations")
    
    if recommendations['sector_allocation']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sector Allocation**")
            allocation_data = pd.DataFrame([
                {'Sector': sector, 'Weight': weight}
                for sector, weight in recommendations['sector_allocation'].items()
            ])
            
            fig_allocation = px.pie(
                allocation_data,
                values='Weight',
                names='Sector',
                title="Recommended Sector Allocation"
            )
            st.plotly_chart(fig_allocation, use_container_width=True)
        
        with col2:
            st.markdown("**Risk Assessment**")
            if recommendations['risk_assessment']:
                risk_data = recommendations['risk_assessment']
                st.metric("Portfolio Beta", f"{risk_data['portfolio_beta']:.2f}")
                st.metric("Risk Level", risk_data['risk_level'])
            
            st.markdown("**Top Stock Picks**")
            if screened_stocks:
                top_picks = pd.DataFrame([
                    {
                        'Symbol': s['symbol'],
                        'Score': s['overall_score'],
                        'Recommendation': s['recommendation']
                    }
                    for s in screened_stocks[:5]
                ])
                st.dataframe(top_picks, use_container_width=True)
    
    st.markdown("---")
    
    # Individual stock analysis
    st.subheader("🔍 Individual Stock Analysis")
    
    if screened_stocks:
        selected_stock = st.selectbox(
            "Select a stock for detailed analysis",
            [s['symbol'] for s in screened_stocks]
        )
        
        if selected_stock:
            stock_data = next(s for s in screened_stocks if s['symbol'] == selected_stock)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{selected_stock} Analysis**")
                st.metric("Overall Score", f"{stock_data['overall_score']:.1f}")
                st.metric("Fundamental Score", f"{stock_data['fundamental_score']:.1f}")
                st.metric("Technical Score", f"{stock_data['technical_score']:.1f}")
                st.metric("Recommendation", stock_data['recommendation'])
                
                # Fundamental data
                fundamental_data = stock_data['fundamental_data']
                if fundamental_data:
                    st.markdown("**Fundamental Data**")
                    st.write(f"Market Cap: ${fundamental_data.get('market_cap', 0):,.0f}")
                    st.write(f"PE Ratio: {fundamental_data.get('pe_ratio', 0):.2f}")
                    st.write(f"ROE: {fundamental_data.get('roe', 0):.2%}")
                    st.write(f"Sector: {fundamental_data.get('sector', 'Unknown')}")
            
            with col2:
                # Trading signals
                st.markdown("**Trading Signals**")
                if stock_data['signals']:
                    for signal in stock_data['signals']:
                        signal_color = "🟢" if signal['type'] == 'BUY' else "🔴"
                        st.write(f"{signal_color} {signal['type']} - {signal['indicator']} ({signal['strength']})")
                        st.write(f"   {signal['reason']}")
                else:
                    st.write("No trading signals at this time")
                
                # Score breakdowns
                if 'fundamental_breakdown' in stock_data:
                    st.markdown("**Fundamental Breakdown**")
                    for category, score in stock_data['fundamental_breakdown'].items():
                        st.write(f"{category.replace('_', ' ').title()}: {score:.1f}")

if __name__ == "__main__":
    main()